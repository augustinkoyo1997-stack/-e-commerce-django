// ====================== CATALOGUE PRODUITS ======================
let productsStatic = [];

// Chargement des produits depuis l'API Django
async function loadProductsFromAPI() {
    try {
        const response = await fetch('/api/products/');
        const data = await response.json();
        productsStatic = data;
        if (currentPage === "home") renderHomeSections(globalSearchTerm);
        else renderCategoryPage(currentPage, globalSearchTerm, currentSubCategory);
    } catch (error) {
        console.error("Erreur chargement produits :", error);
        productsStatic = [];
    }
}

// ====================== GESTION DES VENTES (côté serveur) ======================
async function recordSaleOnServer(productId, quantity) {
    try {
        const response = await fetch('/api/record-sale/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ product_id: productId, quantity: quantity })
        });
        const result = await response.json();
        if (result.status !== 'ok') {
            console.warn('Erreur enregistrement vente :', result.error);
        }
    } catch (error) {
        console.error('Erreur réseau recordSale :', error);
    }
}

// ====================== PANIER ======================
let cart = [];

function saveCart() {
    localStorage.setItem('dipitaCartBenin', JSON.stringify(cart));
}

function loadCart() {
    const stored = localStorage.getItem('dipitaCartBenin');
    if (stored) try { cart = JSON.parse(stored); } catch(e) { cart = []; }
    else cart = [];
    updateCartUI();
}

function updateCartUI() {
    const count = cart.reduce((s,i) => s + i.quantity, 0);
    const cartCountElem = document.getElementById('cartCount');
    if (cartCountElem) cartCountElem.innerText = count;
    renderCartDrawer();
    saveCart();
}

function addToCart(productId) {
    const product = productsStatic.find(p => p.id === productId);
    if (!product) return;
    const exists = cart.find(i => i.id === productId);
    if (exists) exists.quantity += 1;
    else cart.push({ id: product.id, quantity: 1, product: product });
    updateCartUI();
    showToast(`✅ ${product.name} ajouté`);
}

function updateQuantity(id, delta) {
    const idx = cart.findIndex(i => i.id === id);
    if (idx !== -1) {
        const newQty = cart[idx].quantity + delta;
        if (newQty <= 0) cart.splice(idx,1);
        else cart[idx].quantity = newQty;
        updateCartUI();
    }
}

function removeItem(id) {
    cart = cart.filter(i => i.id !== id);
    updateCartUI();
    showToast("Produit retiré");
}

// ====================== RENDU DU PANIER (VERSION CORRIGÉE) ======================
function renderCartDrawer() {
    const container = document.getElementById('cartItemsList');
    if (!container) return;

    if (cart.length === 0) {
        container.innerHTML = `
            <div class="empty-cart">
                <i class="fas fa-shopping-cart"></i>
                <p>Votre panier est vide</p>
            </div>`;
        const totalPriceElem = document.getElementById('cartTotalPrice');
        if (totalPriceElem) totalPriceElem.innerText = '0 CFA';
        return;
    }

    let html = '', total = 0;
    for (let item of cart) {
        const p = item.product;
        total += p.price * item.quantity;
        html += `
            <div class="cart-item" data-id="${p.id}">
                <img class="cart-item-img" src="${p.image}" alt="${p.name}">
                <div class="cart-item-details">
                    <strong>${escapeHtml(p.name)}</strong>
                    <div class="price">${p.price.toLocaleString()} CFA</div>
                    <div class="cart-qty">
                        <button class="qty-minus" data-id="${p.id}">-</button>
                        <span>${item.quantity}</span>
                        <button class="qty-plus" data-id="${p.id}">+</button>
                        <button class="remove-item" data-id="${p.id}">
                            <i class="fas fa-trash-alt"></i>
                        </button>
                    </div>
                </div>
            </div>`;
    }

    container.innerHTML = html;
    const totalPriceElem = document.getElementById('cartTotalPrice');
    if (totalPriceElem) totalPriceElem.innerText = total.toLocaleString() + ' CFA';

    // Réattacher les événements
    document.querySelectorAll('.qty-minus').forEach(btn =>
        btn.addEventListener('click', (e) => updateQuantity(parseInt(btn.dataset.id), -1)));
    document.querySelectorAll('.qty-plus').forEach(btn =>
        btn.addEventListener('click', (e) => updateQuantity(parseInt(btn.dataset.id), 1)));
    document.querySelectorAll('.remove-item').forEach(btn =>
        btn.addEventListener('click', (e) => removeItem(parseInt(btn.dataset.id))));
}

// Fonction utilitaire pour éviter les injections XSS
function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/[&<>]/g, function(m) {
        if (m === '&') return '&amp;';
        if (m === '<') return '&lt;';
        if (m === '>') return '&gt;';
        return m;
    });
}

function showToast(msg) {
    const t = document.getElementById('toastMsg');
    if (!t) return;
    t.innerText = msg;
    t.style.opacity = '1';
    setTimeout(() => t.style.opacity = '0', 2000);
}

// ====================== PAIEMENT STRIPE ======================
async function checkoutStripe() {
    if (cart.length === 0) {
        showToast("Panier vide");
        return;
    }
    const payload = {
        cart: cart.map(item => ({ id: item.id, quantity: item.quantity }))
    };
    try {
        const response = await fetch('/payments/create-checkout-session/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await response.json();
        if (data.url) {
            window.location.href = data.url;
        } else {
            showToast("Erreur Stripe : " + (data.error || "inconnue"));
        }
    } catch (error) {
        console.error("Erreur réseau :", error);
        showToast("Erreur de connexion, veuillez réessayer.");
    }
}

// ====================== PAIEMENT KKIAPAY (Mobile Money) ======================
async function loadKkiapayScript() {
    return new Promise((resolve, reject) => {
        if (typeof Kkiapay !== 'undefined') {
            resolve();
            return;
        }
        const script = document.createElement('script');
        script.src = 'https://cdn.kkiapay.me/sdk/kkiapay.js';
        script.onload = () => resolve();
        script.onerror = () => reject(new Error("Impossible de charger KKiaPay"));
        document.head.appendChild(script);
    });
}

async function openKkiapayWidget(amount) {
    await loadKkiapayScript();
    Kkiapay({
        publicKey: KKIAY_PUBLIC_KEY,
        sandbox: KKIAY_SANDBOX,
        amount: amount,
        currency: 'XOF',
        callback: (result) => {
            console.log('Paiement KKiaPay réussi', result);
            showToast("✅ Paiement accepté !");
            cart = [];
            updateCartUI();
            if (currentPage === "home") renderHomeSections(globalSearchTerm);
            else renderCategoryPage(currentPage, globalSearchTerm, currentSubCategory);
            if (typeof closeDrawer === 'function') closeDrawer();
            window.location.href = '/payments/success/';
        },
        onClose: () => {
            console.log('Widget KKiaPay fermé');
        }
    });
}

async function checkoutMomo() {
    if (cart.length === 0) {
        showToast("Panier vide");
        return;
    }
    const total = cart.reduce((sum, item) => sum + (item.product.price * item.quantity), 0);
    await openKkiapayWidget(total);
}

// ====================== AFFICHAGE DES PRODUITS ======================
function renderProductList(productsArray, containerId, showSalesBadge = false) {
    const container = document.getElementById(containerId);
    if (!container) return;
    if (productsArray.length === 0) {
        container.innerHTML = `<div style="grid-column:1/-1; padding:40px; text-align:center;">Aucun produit trouvé</div>`;
        return;
    }
    let html = '';
    productsArray.forEach(p => {
        const stars = '★'.repeat(Math.floor(p.rating)) + '☆'.repeat(5 - Math.floor(p.rating));
        let badges = '';
        if (p.isNew) badges += `<div class="badge-new">🆕 Nouveau</div>`;
        let salesInfo = '';
        if (showSalesBadge && p.salesCount > 0) salesInfo = `<div class="sales-count">📊 ${p.salesCount} vendu(s)</div>`;
        html += `<div class="product-card">
                    ${badges}
                    ${salesInfo}
                    <img class="product-img" src="${p.image}" alt="${p.name}" loading="lazy">
                    <div class="product-info">
                        <div class="product-title">${escapeHtml(p.name)}</div>
                        <div class="supplier"><i class="fas fa-store"></i> ${escapeHtml(p.supplier)}</div>
                        <div class="price">${p.price.toLocaleString()} CFA</div>
                        <div class="rating">${stars} ${p.rating}</div>
                        <button class="add-cart" data-id="${p.id}"><i class="fas fa-cart-plus"></i> Ajouter</button>
                    </div>
                </div>`;
    });
    container.innerHTML = html;
    container.querySelectorAll('.add-cart').forEach(btn => btn.addEventListener('click', (e) => addToCart(parseInt(btn.dataset.id))));
}

// ====================== SOUS-CATÉGORIES ======================
let currentSubCategory = "all";

const subCategoriesMap = {
    Smartphone: ["all", "Samsung", "iPhone", "Tecno", "Infinix", "Huawei", "Google Pixel", "Itel", "Xiaomi"],
    Electronique: ["all", "Audio", "Périphériques"],
    Electromenager: ["all", "Petit électroménager", "Gros électroménager", "Entretien"],
    Verres: ["all", "Verres à vin", "Verres à eau", "Coupes"],
    PC: ["all", "Portable Dell", "Portable HP", "Portable Lenovo", "Ordinateur fixe"],
    Textile: ["all", "Wax", "Bazin", "Bogolan"],
    Artisanat: ["all", "Décoration", "Sculpture", "Vannerie"]
};

function renderSubCategoryButtons(category) {
    const containerId = `subcat-${category.toLowerCase()}`;
    const container = document.getElementById(containerId);
    if (!container) return;
    const subcats = subCategoriesMap[category] || ["all"];
    let html = `<span style="font-size:0.8rem; font-weight:600; margin-right:8px;">Filtrer :</span>`;
    subcats.forEach(sub => {
        const activeClass = (currentSubCategory === sub) ? 'active' : '';
        const displayName = sub === "all" ? "Toutes" : sub;
        html += `<button class="subcat-btn ${activeClass}" data-subcat="${sub}">${displayName}</button>`;
    });
    container.innerHTML = html;
    container.querySelectorAll('.subcat-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            currentSubCategory = btn.getAttribute('data-subcat');
            renderCategoryPage(currentPage, globalSearchTerm, currentSubCategory);
            container.querySelectorAll('.subcat-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });
}

function renderCategoryPage(pageId, search = "", subCat = "all") {
    let filtered = productsStatic.filter(p => p.category === pageId);
    if (search.trim() !== "") {
        const term = search.trim().toLowerCase();
        filtered = filtered.filter(p => p.name.toLowerCase().includes(term) || p.supplier.toLowerCase().includes(term));
    }
    if (subCat !== "all") {
        filtered = filtered.filter(p => p.subCategory === subCat);
    }
    let containerId = "";
    if (pageId === "Electronique") containerId = "electronique-products";
    else if (pageId === "Electromenager") containerId = "electromenager-products";
    else if (pageId === "Smartphone") containerId = "smartphone-products";
    else if (pageId === "Verres") containerId = "verres-products";
    else if (pageId === "PC") containerId = "pc-products";
    else if (pageId === "Textile") containerId = "textile-products";
    else if (pageId === "Artisanat") containerId = "artisanat-products";
    else return;
    renderProductList(filtered, containerId, false);
    renderSubCategoryButtons(pageId);
}

function renderHomeSections(search = "") {
    let allProducts = productsStatic;
    if (search.trim() !== "") {
        const term = search.trim().toLowerCase();
        allProducts = allProducts.filter(p => p.name.toLowerCase().includes(term) || p.supplier.toLowerCase().includes(term));
    }
    const newProds = allProducts.filter(p => p.isNew === true);
    const topSellers = [...allProducts].sort((a,b) => b.salesCount - a.salesCount).filter(p => p.salesCount > 0);
    renderProductList(newProds, "new-products", false);
    renderProductList(topSellers, "top-products", true);
    renderProductList(allProducts, "home-products", false);
}

// ====================== NAVIGATION ======================
let currentPage = "home";
let globalSearchTerm = "";
let closeDrawer = null;

function setActivePage(pageId) {
    document.querySelectorAll('.page').forEach(page => page.classList.remove('active-page'));
    const target = document.getElementById(`page-${pageId}`);
    if (target) target.classList.add('active-page');
    document.querySelectorAll('.page-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.page === pageId) btn.classList.add('active');
    });
    currentPage = pageId;
    if (pageId === "home") {
        renderHomeSections(globalSearchTerm);
    } else {
        currentSubCategory = "all";
        renderCategoryPage(pageId, globalSearchTerm, "all");
    }
    const menu = document.getElementById('pageLinks');
    if (window.innerWidth <= 800 && menu && menu.classList.contains('open')) menu.classList.remove('open');
}

function applyGlobalSearch() {
    const searchInput = document.getElementById('globalSearch');
    if (searchInput) globalSearchTerm = searchInput.value;
    if (currentPage === "home") renderHomeSections(globalSearchTerm);
    else renderCategoryPage(currentPage, globalSearchTerm, currentSubCategory);
}

// ====================== MENU HAMBURGER & PANIER ======================
function initDrawer() {
    const cartIcon = document.getElementById('cartIcon');
    const overlay = document.getElementById('cartOverlay');
    const drawer = document.getElementById('cartDrawer');
    const closeBtn = document.getElementById('closeCartBtn');
    const openDrawer = () => {
        if (overlay) overlay.classList.add('open');
        if (drawer) drawer.classList.add('open');
    };
    closeDrawer = () => {
        if (overlay) overlay.classList.remove('open');
        if (drawer) drawer.classList.remove('open');
    };
    if (cartIcon) cartIcon.onclick = openDrawer;
    if (overlay) overlay.onclick = closeDrawer;
    if (closeBtn) closeBtn.onclick = closeDrawer;

    const stripeBtn = document.getElementById('checkoutStripeBtn');
    if (stripeBtn) stripeBtn.onclick = () => checkoutStripe();
    const momoBtn = document.getElementById('checkoutMomoBtn');
    if (momoBtn) momoBtn.onclick = () => checkoutMomo();
}

function initHamburger() {
    const hamburger = document.getElementById('hamburgerBtn');
    const menu = document.getElementById('pageLinks');
    if (hamburger && menu) {
        hamburger.addEventListener('click', (e) => {
            e.stopPropagation();
            menu.classList.toggle('open');
        });
        document.addEventListener('click', function(event) {
            if (!menu.contains(event.target) && !hamburger.contains(event.target)) {
                menu.classList.remove('open');
            }
        });
    }
}

function initNavigation() {
    document.querySelectorAll('.page-btn').forEach(btn => btn.addEventListener('click', () => setActivePage(btn.dataset.page)));
    const searchBtn = document.getElementById('searchBtn');
    if (searchBtn) searchBtn.addEventListener('click', applyGlobalSearch);
    const globalSearch = document.getElementById('globalSearch');
    if (globalSearch) globalSearch.addEventListener('keypress', (e) => { if (e.key === 'Enter') applyGlobalSearch(); });
}

// ====================== DÉMARRAGE ======================
async function start() {
    loadCart();
    initDrawer();
    initNavigation();
    initHamburger();
    await loadProductsFromAPI();
    setActivePage("home");
}

// Ajouter au panier depuis page détail
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('add-to-cart-detail')) {
        const productId = parseInt(e.target.dataset.id);
        const quantity = parseInt(document.getElementById('product-quantity').value);
        for(let i = 0; i < quantity; i++) {
            addToCart(productId);
        }
        showToast(`✅ Produit ajouté (${quantity})`);
    }
});

start();