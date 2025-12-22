const ORDER_STORAGE_KEY = "pendingOrder";

function readOrder() {
  try {
    return JSON.parse(localStorage.getItem(ORDER_STORAGE_KEY) || "null") || { products: {}, cartItems: [] };
  } catch {
    return { products: {}, cartItems: [] };
  }
}

function writeOrder(order) {
  try {
    localStorage.setItem(ORDER_STORAGE_KEY, JSON.stringify(order));
    updateCartBadge();
  } catch (e) {
    console.error("Failed to save order", e);
  }
}

function normalizeInt(v) {
  const n = parseInt(v, 10);
  return Number.isFinite(n) && n > 0 ? n : 0;
}

function updateCartBadge() {
  const badge = document.getElementById("cartCount");
  if (!badge) return;

  const order = readOrder();
  const totalQty = Object.values(order.products || {}).reduce((acc, x) => acc + normalizeInt(x), 0);
  badge.textContent = String(totalQty);
}

function ensureSkeletons() {
  document.querySelectorAll("img[data-skeleton]").forEach((img) => {
    const parent = img.closest(".product-media");
    if (!parent) return;

    if (img.complete) return;

    let sk = parent.querySelector(".skeleton");
    if (!sk) {
      sk = document.createElement("div");
      sk.className = "skeleton";
      parent.appendChild(sk);
    }

    img.addEventListener(
      "load",
      () => {
        sk?.remove();
      },
      { once: true }
    );

    img.addEventListener(
      "error",
      () => {
        sk?.remove();
      },
      { once: true }
    );
  });
}

function showToast(message) {
  let toast = document.getElementById("toast-notification");
  if (!toast) {
    toast = document.createElement("div");
    toast.id = "toast-notification";
    toast.style.position = "fixed";
    toast.style.bottom = "20px";
    toast.style.left = "50%";
    toast.style.transform = "translateX(-50%)";
    toast.style.backgroundColor = "#10b981"; // Green
    toast.style.color = "#fff";
    toast.style.padding = "12px 24px";
    toast.style.borderRadius = "8px";
    toast.style.zIndex = "9999";
    toast.style.boxShadow = "0 4px 6px rgba(0,0,0,0.1)";
    toast.style.fontWeight = "bold";
    toast.style.opacity = "0";
    toast.style.transition = "opacity 0.3s ease-in-out";
    toast.style.pointerEvents = "none";
    document.body.appendChild(toast);
  }
  
  toast.textContent = message;
  toast.style.opacity = "1";
  
  // Clear previous timeout if exists
  if (toast.timeoutId) clearTimeout(toast.timeoutId);
  
  toast.timeoutId = setTimeout(() => {
    toast.style.opacity = "0";
  }, 2000);
}

// Public API used by templates
window.storeAddToCart = function storeAddToCart({ id, name, price, imageUrl } = {}) {
  if (!id) return;

  const order = readOrder();
  order.products = order.products || {};
  order.cartItems = order.cartItems || [];

  const key = `product_${id}`;
  order.products[key] = normalizeInt(order.products[key]) + 1;

  const existing = order.cartItems.find((x) => String(x.id) === String(id));
  if (existing) {
    existing.qty = normalizeInt(existing.qty) + 1;
  } else {
    order.cartItems.push({ id, name: name || "", price: Number(price) || 0, imageUrl: imageUrl || "", qty: 1 });
  }

  writeOrder(order);
  showToast("\u062a\u0645\u062a \u0627\u0644\u0625\u0636\u0627\u0641\u0629 \u0644\u0644\u0633\u0644\u0629 \u0628\u0646\u062c\u0627\u062d");
};

window.storeClearCart = function storeClearCart() {
  writeOrder({ products: {}, cartItems: [] });
};

function initCartPage() {
  const root = document.getElementById("cartRoot");
  if (!root) return;

  const list = document.getElementById("cartItems");
  const totalEl = document.getElementById("cartTotal");
  const emptyEl = document.getElementById("cartEmpty");

  const render = () => {
    const order = readOrder();
    const items = (order.cartItems || []).filter((x) => normalizeInt(x.qty) > 0);

    if (emptyEl) emptyEl.style.display = items.length ? "none" : "block";
    if (list) list.innerHTML = "";

    let total = 0;

    for (const it of items) {
      total += (Number(it.price) || 0) * normalizeInt(it.qty);

      const row = document.createElement("div");
      row.className = "card";
      row.style.padding = "12px";
      row.innerHTML = `
        <div style="display:flex;gap:12px;align-items:center;justify-content:space-between;flex-wrap:wrap;">
          <div style="display:flex;gap:12px;align-items:center;min-width:240px;">
            ${it.imageUrl ? `<img src="${it.imageUrl}" alt="" width="56" height="56" style="border-radius:12px;object-fit:cover;" loading="lazy" decoding="async" />` : ``}
            <div>
              <div style="font-weight:950;">${it.name || ""}</div>
              <div style="color:rgba(229,231,235,.70);">${Number(it.price || 0).toFixed(2)} \u062f.\u062a</div>
            </div>
          </div>

          <div style="display:flex;gap:10px;align-items:center;">
            <input class="input" style="max-width:110px" type="number" min="0" value="${normalizeInt(it.qty)}" />
            <button class="btn btn-ghost" type="button">\u062d\u0630\u0641</button>
          </div>
        </div>
      `;

      const qtyInput = row.querySelector("input");
      const delBtn = row.querySelector("button");

      qtyInput?.addEventListener("change", () => {
        const q = normalizeInt(qtyInput.value);
        it.qty = q;
        order.products = order.products || {};
        order.products[`product_${it.id}`] = q;
        order.cartItems = items;
        writeOrder(order);
        render();
      });

      delBtn?.addEventListener("click", () => {
        it.qty = 0;
        order.products = order.products || {};
        order.products[`product_${it.id}`] = 0;
        order.cartItems = items.filter((x) => String(x.id) !== String(it.id));
        writeOrder(order);
        render();
      });

      list?.appendChild(row);
    }

    if (totalEl) totalEl.textContent = `${total.toFixed(2)} \u062f.\u062a`;
  };

  render();

  document.getElementById("cartClear")?.addEventListener("click", () => {
    window.storeClearCart();
    render();
  });
}

document.addEventListener("DOMContentLoaded", () => {
  updateCartBadge();
  ensureSkeletons();
  initCartPage();
});
