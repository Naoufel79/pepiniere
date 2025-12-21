import { auth, db } from "./firebase.js";
import {
  RecaptchaVerifier,
  signInWithPhoneNumber,
  onAuthStateChanged
} from "https://www.gstatic.com/firebasejs/10.12.5/firebase-auth.js";
import {
  addDoc,
  collection,
  serverTimestamp
} from "https://www.gstatic.com/firebasejs/10.12.5/firebase-firestore.js";

let recaptchaVerifier = null;
let confirmationResult = null;

function $(id) {
  return document.getElementById(id);
}

function setText(id, text) {
  const el = $(id);
  if (el) el.textContent = text;
}

function show(el, shouldShow) {
  if (!el) return;
  el.style.display = shouldShow ? "block" : "none";
}

function setBusy(button, busy) {
  if (!button) return;
  button.disabled = busy;
  button.dataset.originalText ||= button.textContent;
  button.textContent = busy ? "..." : button.dataset.originalText;
}

function normalizePhoneNumber(raw) {
  const trimmed = (raw || "").trim();

  // If user enters Tunisia local number (8 digits), convert to E.164.
  if (/^\d{8}$/.test(trimmed)) {
    return `+216${trimmed}`;
  }

  return trimmed;
}

function getFriendlyAuthError(err) {
  const code = err?.code || "";

  if (code.includes("auth/invalid-phone-number")) return "رقم الهاتف غير صحيح. الرجاء إدخال الرقم بصيغة دولية مثل +21620123456";
  if (code.includes("auth/missing-phone-number")) return "الرجاء إدخال رقم الهاتف.";
  if (code.includes("auth/operation-not-allowed")) return "خدمة التحقق عبر الهاتف غير مفعّلة في Firebase. فعّل Phone Sign-in من Firebase Console ثم أعد المحاولة.";
  if (code.includes("auth/too-many-requests")) return "تم إرسال طلبات كثيرة جدا. الرجاء المحاولة لاحقا.";
  if (code.includes("auth/captcha-check-failed")) return "تعذر التحقق من reCAPTCHA. الرجاء تحديث الصفحة والمحاولة مرة أخرى.";
  if (code.includes("auth/app-not-authorized")) return "التطبيق غير مصرح به لاستخدام Phone Auth. تأكد أنك تستخدم إعدادات Firebase (apiKey / authDomain) الخاصة بمشروع Prod، وأضف دومين Railway ضمن Authorized domains.";
  if (code.includes("auth/unauthorized-domain")) return "هذا الدومين غير مصرح به. أضفه في Firebase Console → Authentication → Settings → Authorized domains ثم أعد المحاولة.";
  if (code.includes("auth/invalid-app-credential")) return "فشل التحقق من بيانات التطبيق (reCAPTCHA/credential). تأكد أن الدومين مصرح به وأن reCAPTCHA غير محجوبة (AdBlock/VPN) ثم أعد المحاولة.";
  if (code.includes("auth/missing-app-credential")) return "reCAPTCHA لم يعمل. حدّث الصفحة ثم أعد المحاولة، وتأكد أن الدومين مصرح به ضمن Firebase Authorized domains.";
  if (code.includes("auth/quota-exceeded")) return "تم تجاوز حصة إرسال رسائل SMS لهذا المشروع. جرّب لاحقاً أو استخدم أرقام اختبار في Firebase.";
  if (code.includes("auth/billing-not-enabled")) return "خدمة SMS تتطلب تفعيل الفوترة (Billing) لهذا المشروع على Google Cloud/Firebase. فعّل Billing (Blaze/حساب فوترة) أو استخدم أرقام الاختبار في Firebase أثناء التطوير.";
  if (code.includes("auth/invalid-verification-code")) return "رمز التحقق غير صحيح.";
  if (code.includes("auth/code-expired")) return "انتهت صلاحية الرمز. الرجاء طلب رمز جديد.";

  if (code) return `حدث خطأ (${code}). الرجاء المحاولة مرة أخرى.`;
  const msg = err?.message || "";
  if (msg) return `حدث خطأ: ${msg}`;
  return "حدث خطأ. الرجاء المحاولة مرة أخرى.";
}

function setAuthMessage({ error = "", success = "", status = "" } = {}) {
  const errorEl = $("phoneAuthError");
  const successEl = $("phoneAuthSuccess");
  const statusEl = $("phoneAuthStatus");

  setText("phoneAuthError", error);
  setText("phoneAuthSuccess", success);
  setText("phoneAuthStatus", status);

  show(errorEl, Boolean(error));
  show(successEl, Boolean(success));
  show(statusEl, Boolean(status));
}

async function ensureRecaptcha() {
  if (recaptchaVerifier) return recaptchaVerifier;

  const container = $("recaptcha-container");
  if (!container) {
    throw new Error("Missing reCAPTCHA container");
  }

  recaptchaVerifier = new RecaptchaVerifier(auth, "recaptcha-container", {
    size: "invisible"
  });

  await recaptchaVerifier.render();
  return recaptchaVerifier;
}

function setVerifiedUI(user) {
  const placeOrderBtn = $("placeOrderBtn");
  const sendOtpBtn = $("sendOtpBtn");
  const verifyOtpBtn = $("verifyOtpBtn");
  const verifySection = $("verifySection");

  const telephoneInput = $("telephone");
  if (telephoneInput && user?.phoneNumber) {
    telephoneInput.value = user.phoneNumber;
    telephoneInput.readOnly = true;
  }

  if (sendOtpBtn) sendOtpBtn.disabled = true;
  if (verifyOtpBtn) verifyOtpBtn.disabled = true;
  show(verifySection, false);

  if (placeOrderBtn) placeOrderBtn.disabled = false;

  setAuthMessage({
    success: "\u2713 تم تأكيد رقم الهاتف بنجاح",
    status: user?.phoneNumber ? `رقم الهاتف: ${user.phoneNumber}` : "تم تأكيد رقم الهاتف"
  });
}

function setNotVerifiedUI() {
  const placeOrderBtn = $("placeOrderBtn");
  const sendOtpBtn = $("sendOtpBtn");
  const verifyOtpBtn = $("verifyOtpBtn");

  const telephoneInput = $("telephone");
  if (telephoneInput) {
    telephoneInput.readOnly = false;
  }

  if (placeOrderBtn) placeOrderBtn.disabled = true;
  if (sendOtpBtn) sendOtpBtn.disabled = false;
  if (verifyOtpBtn) verifyOtpBtn.disabled = false;

  setAuthMessage({
    status: "الرجاء تأكيد رقم الهاتف عبر رسالة SMS لإرسال الطلب."
  });
}

function getSelectedItems() {
  const quantities = document.querySelectorAll(".product-quantity");
  const items = [];
  let total = 0;

  quantities.forEach((input) => {
    const qty = parseInt(input.value, 10) || 0;
    if (qty <= 0) return;

    const id = (input.id || "").replace(/^product_/, "");
    const name = input.getAttribute("data-product-name") || "";
    const price = parseFloat(input.getAttribute("data-product-price") || "0") || 0;

    items.push({
      productId: id,
      name,
      qty,
      price
    });

    total += qty * price;
  });

  return { items, total };
}

async function sendOtp() {
  const phoneRaw = $("telephone")?.value;
  const phoneNumber = normalizePhoneNumber(phoneRaw);

  if (!phoneNumber) {
    setAuthMessage({ error: "الرجاء إدخال رقم الهاتف." });
    return;
  }

  if (!phoneNumber.startsWith("+")) {
    setAuthMessage({ error: "الرجاء إدخال الرقم بصيغة دولية (E.164) مثل +21620123456" });
    return;
  }

  // Basic E.164 sanity check (+ and 8-15 digits).
  if (!/^\+\d{8,15}$/.test(phoneNumber)) {
    setAuthMessage({ error: "رقم الهاتف غير صحيح. مثال صحيح: +21620123456" });
    return;
  }

  // Tunisia numbers must be +216 followed by 8 digits.
  if (phoneNumber.startsWith("+216") && !/^\+216\d{8}$/.test(phoneNumber)) {
    setAuthMessage({ error: "رقم تونس يجب أن يكون +216 متبوعاً بـ 8 أرقام (مثال: +21620123456)" });
    return;
  }

  const sendBtn = $("sendOtpBtn");
  setBusy(sendBtn, true);
  setAuthMessage({ status: "جاري إرسال الرمز..." });

  try {
    const appVerifier = await ensureRecaptcha();
    confirmationResult = await signInWithPhoneNumber(auth, phoneNumber, appVerifier);

    show($("verifySection"), true);
    setAuthMessage({
      success: "تم إرسال رمز التحقق عبر SMS.",
      status: "أدخل الرمز المكون من 6 أرقام."
    });
  } catch (err) {
    console.error(err);
    // If reCAPTCHA gets into a bad state, reset it
    try {
      recaptchaVerifier?.clear();
    } catch (_) {
      // ignore
    }
    recaptchaVerifier = null;

    setAuthMessage({ error: getFriendlyAuthError(err) });
  } finally {
    setBusy(sendBtn, false);
  }
}

async function verifyOtp() {
  const code = ($("otpCode")?.value || "").trim();
  const verifyBtn = $("verifyOtpBtn");

  if (!confirmationResult) {
    setAuthMessage({ error: "الرجاء طلب الرمز أولا." });
    return;
  }

  if (!/^\d{6}$/.test(code)) {
    setAuthMessage({ error: "الرجاء إدخال رمز مكون من 6 أرقام." });
    return;
  }

  setBusy(verifyBtn, true);
  setAuthMessage({ status: "جاري التحقق من الرمز..." });

  try {
    const cred = await confirmationResult.confirm(code);
    setVerifiedUI(cred.user);
  } catch (err) {
    console.error(err);
    setAuthMessage({ error: getFriendlyAuthError(err) });
  } finally {
    setBusy(verifyBtn, false);
  }
}

async function handlePlaceOrder(e) {
  e.preventDefault();

  const user = auth.currentUser;
  if (!user) {
    setAuthMessage({ error: "يجب تأكيد رقم الهاتف أولا." });
    window.scrollTo({ top: 0, behavior: "smooth" });
    return;
  }

  const { items, total } = getSelectedItems();
  if (!items.length) {
    alert("الرجاء اختيار منتج واحد على الأقل");
    return;
  }

  const confirmed = confirm("هل أنت متأكد من إرسال طلبك\n\nسيتم إرسال طلبك وسنتصل بك قريبا.");
  if (!confirmed) return;

  const placeOrderBtn = $("placeOrderBtn");
  const orderForm = $("orderForm");

  setBusy(placeOrderBtn, true);
  setAuthMessage({ status: "جاري تسجيل الطلب..." });

  try {
    const tokenInput = $("firebase_id_token");
    if (tokenInput) {
      tokenInput.value = await user.getIdToken();
    }

    const orderDoc = {
      uid: user.uid,
      phoneNumber: user.phoneNumber || "",
      items,
      total,
      status: "pending",
      createdAt: serverTimestamp(),

      // Optional extra info for your ops
      customerName: $("nom")?.value || "",
      wilaya: $("wilaya")?.value || "",
      ville: $("ville")?.value || "",
      email: ($("email")?.value || "").trim() || null
    };

    await addDoc(collection(db, "orders"), orderDoc);

    // Keep the existing Django flow (stock decrement + email) by submitting the form.
    if (typeof window.clearOrderFromStorage === "function") {
      window.clearOrderFromStorage();
    }

    orderForm.submit();
  } catch (err) {
    console.error(err);
    setAuthMessage({ error: "تعذر حفظ الطلب. الرجاء المحاولة مرة أخرى." });
    setBusy(placeOrderBtn, false);
  }
}

function init() {
  const sendBtn = $("sendOtpBtn");
  const verifyBtn = $("verifyOtpBtn");
  const orderForm = $("orderForm");

  if (sendBtn) sendBtn.addEventListener("click", sendOtp);
  if (verifyBtn) verifyBtn.addEventListener("click", verifyOtp);
  if (orderForm) orderForm.addEventListener("submit", handlePlaceOrder);

  onAuthStateChanged(auth, (user) => {
    if (user?.phoneNumber) {
      setVerifiedUI(user);
    } else {
      setNotVerifiedUI();
    }
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}




