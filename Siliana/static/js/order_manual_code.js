function $(id) {
  return document.getElementById(id);
}

function setStepperState(verified) {
  const s1 = $("step1");
  const s2 = $("step2");
  const s3 = $("step3");
  if (!s1 || !s2 || !s3) return;

  // In static-code mode, we let the user fill delivery/products normally.
  // This stepper only indicates whether verification is complete.
  s2.classList.add("is-active");
  s3.classList.add("is-active");

  if (verified) {
    s1.classList.remove("is-active");
    s1.classList.add("is-done");
  } else {
    s1.classList.add("is-active");
    s1.classList.remove("is-done");
  }
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

function setMessage({ error = "", success = "", status = "" } = {}) {
  const errorEl = $("manualCodeError");
  const successEl = $("manualCodeSuccess");
  const statusEl = $("manualCodeStatus");

  setText("manualCodeError", error);
  setText("manualCodeSuccess", success);
  setText("manualCodeStatus", status);

  show(errorEl, Boolean(error));
  show(successEl, Boolean(success));
  show(statusEl, Boolean(status));
}

function init() {
  const verifyBtn = $("verifyManualCodeBtn");
  const placeOrderBtn = $("placeOrderBtn");
  const codeInput = $("manualCode");

  if (!verifyBtn || !placeOrderBtn || !codeInput) return;

  placeOrderBtn.disabled = true;
  setStepperState(false);
  setMessage({ status: "في الخطوة الأخيرة أدخل الرمز لتفعيل زر تأكيد الطلب." });

  verifyBtn.addEventListener("click", () => {
    const code = (window.prompt("أدخل رمز التأكيد") || "").trim();

    if (!code) {
      setMessage({ error: "الرجاء إدخال الرمز." });
      return;
    }

    // Basic validation only; server enforces the real check.
    if (!/^\d{4,12}$/.test(code)) {
      setMessage({ error: "الرمز غير صحيح. أدخل أرقام فقط." });
      return;
    }

    // Store for POST; server enforces the real check.
    codeInput.value = code;

    verifyBtn.disabled = true;
    verifyBtn.textContent = "تم إدخال الرمز";

    placeOrderBtn.disabled = false;
    setStepperState(true);

    setMessage({
      success: "تم إدخال الرمز. يمكنك الآن إرسال الطلب.",
      status: "عند إرسال الطلب سيتم التحقق من الرمز.",
    });
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}
