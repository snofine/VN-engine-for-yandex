// yandex_sdk.js - Production-Ready Yandex Games SDK Integration
let ysdk = null;
let payments = null;
let isAdsDisabled = false;

// Callbacks to be set by the game engine
let onAdOpenCallback = null;
let onAdCloseCallback = null;
let onPurchaseSuccessCallback = null;

// Initialize Yandex SDK
async function initYandexSDK(purchaseId) {
    console.log("Initializing Yandex SDK...");
    try {
        if (typeof YaGames !== 'undefined') {
            ysdk = await YaGames.init();
            console.log("Yandex SDK initialized successfully.");
            
            // Try to initialize payments if purchaseId is provided
            if (purchaseId) {
                await initPayments(purchaseId);
            }
            return true;
        } else {
            console.warn("Yandex SDK is not available (running locally or blocked). Using Mock SDK.");
            return false;
        }
    } catch (error) {
        console.error("Error during Yandex SDK initialization:", error);
        return false;
    }
}

// Initialize payments
async function initPayments(purchaseId) {
    if (!ysdk) return;
    try {
        payments = await ysdk.getPayments({ signed: true });
        console.log("Payments initialized.");
        if (purchaseId) {
            await checkPurchases(purchaseId);
        }
    } catch (err) {
        console.error("Payments initialization failed:", err);
        // Payments initialization might fail if user is not authorized,
        // we will handle authorization flow during the purchase request.
    }
}

// Check if player has already purchased the ad removal
async function checkPurchases(purchaseId) {
    if (!payments) return;
    try {
        const purchases = await payments.getPurchases();
        const hasNoAds = purchases.some(purchase => purchase.productID === purchaseId);
        if (hasNoAds) {
            console.log("In-App Purchase found: Ads are disabled.");
            isAdsDisabled = true;
            if (onPurchaseSuccessCallback) {
                onPurchaseSuccessCallback();
            }
        } else {
            console.log("In-App Purchase not found: Ads are enabled.");
        }
    } catch (err) {
        console.error("Error checking purchases:", err);
    }
}

// Show Fullscreen Ad
function showFullscreenAd() {
    if (isAdsDisabled) {
        console.log("Skipping ad: Ads are disabled by In-App Purchase.");
        return;
    }
    
    console.log("Requesting Fullscreen Ad...");
    
    if (ysdk) {
        ysdk.adv.showFullscreenAdv({
            callbacks: {
                onOpen: () => {
                    console.log("Ad opened.");
                    if (onAdOpenCallback) onAdOpenCallback();
                },
                onClose: (wasShown) => {
                    console.log("Ad closed. Was shown:", wasShown);
                    if (onAdCloseCallback) onAdCloseCallback(wasShown);
                },
                onError: (error) => {
                    console.error("Ad error:", error);
                    if (onAdCloseCallback) onAdCloseCallback(false);
                },
                onOffline: () => {
                    console.warn("Ad offline.");
                    if (onAdCloseCallback) onAdCloseCallback(false);
                }
            }
        });
    } else {
        // Mock ad behavior for local testing
        console.log("[Mock Ad] Displaying full screen ad simulator for 3 seconds...");
        if (onAdOpenCallback) onAdOpenCallback();
        createMockAdOverlay();
    }
}

// Create a mock ad overlay for local testing
function createMockAdOverlay() {
    if (document.getElementById('mock-ad-overlay')) return;

    const overlay = document.createElement('div');
    overlay.id = 'mock-ad-overlay';
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100vw';
    overlay.style.height = '100vh';
    overlay.style.background = 'rgba(0,0,0,0.95)';
    overlay.style.color = 'white';
    overlay.style.display = 'flex';
    overlay.style.flexDirection = 'column';
    overlay.style.justifyContent = 'center';
    overlay.style.alignItems = 'center';
    overlay.style.zIndex = '99999';
    overlay.style.fontFamily = 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
    
    overlay.innerHTML = `
        <div style="background: #1a1a1a; padding: 30px; border-radius: 12px; border: 1px solid #333; text-align: center; max-width: 400px; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
            <h2 style="margin: 0 0 15px 0; color: #ffcc00; font-size: 24px;">РЕКЛАМА (MOCK SDK)</h2>
            <p style="margin: 0 0 10px 0; font-size: 16px; color: #ccc;">Это симуляция полноэкранной рекламы Яндекс.Игр для тестирования на ПК.</p>
            <p id="mock-timer" style="margin: 15px 0; font-size: 18px; font-weight: bold; color: #66ff66;">Закроется через 3 сек...</p>
            <button id="mock-close-btn" style="display:none; margin: 15px auto 0 auto; padding:10px 25px; font-size:16px; cursor:pointer; background:#ffcc00; color:#000; border:none; border-radius:6px; font-weight:bold; transition: background 0.2s;">Закрыть рекламу</button>
        </div>
    `;
    
    document.body.appendChild(overlay);
    
    let secondsLeft = 3;
    const interval = setInterval(() => {
        secondsLeft--;
        const timerText = document.getElementById('mock-timer');
        if (timerText) {
            timerText.innerText = `Закроется через ${secondsLeft} сек...`;
        }
        if (secondsLeft <= 0) {
            clearInterval(interval);
            const closeBtn = document.getElementById('mock-close-btn');
            if (closeBtn) {
                closeBtn.style.display = 'block';
                const timerText = document.getElementById('mock-timer');
                if (timerText) timerText.style.display = 'none';
            }
        }
    }, 1000);
    
    const closeAd = () => {
        if (document.body.contains(overlay)) {
            document.body.removeChild(overlay);
        }
        console.log("Mock ad closed.");
        if (onAdCloseCallback) onAdCloseCallback(true);
    };
    
    const closeBtn = document.getElementById('mock-close-btn');
    if (closeBtn) {
        closeBtn.onclick = closeAd;
    }
}

// Purchase "Remove Ads" using production API with authorization checks
async function purchaseRemoveAds(purchaseId) {
    if (isAdsDisabled) {
        console.log("Ads are already disabled.");
        return;
    }
    
    console.log("Initiating purchase for:", purchaseId);
    if (!ysdk) {
        // Mock purchase success for testing
        console.log("[Mock Purchase] Simulating successful purchase of:", purchaseId);
        const confirmPurchase = confirm("[MOCK PURCHASE]\nХотите симулировать успешную покупку 'Отключение рекламы'?");
        if (confirmPurchase) {
            isAdsDisabled = true;
            if (onPurchaseSuccessCallback) {
                onPurchaseSuccessCallback();
            }
            alert("Реклама отключена! (Симуляция)");
        }
        return;
    }

    try {
        // Try initializing payments if not ready
        if (!payments) {
            payments = await ysdk.getPayments({ signed: true });
        }
        
        await payments.purchase({ id: purchaseId });
        console.log("Purchase successful!");
        isAdsDisabled = true;
        if (onPurchaseSuccessCallback) {
            onPurchaseSuccessCallback();
        }
        alert("Реклама отключена! Спасибо за покупку.");
    } catch (err) {
        console.error("Purchase failed or encountered error:", err);
        
        if (err.code === 'CLIENT_OFFLINE') {
            alert("Ошибка сети: Проверьте подключение к интернету для проведения оплаты.");
        } else if (err.code === 'NO_SIGN_IN') {
            // Player is not logged in. Prompt them to log in via auth dialog.
            const confirmLogin = confirm("Для совершения покупок необходимо авторизоваться в Яндексе. Войти сейчас?");
            if (confirmLogin) {
                try {
                    await ysdk.auth.openAuthDialog();
                    console.log("Player authorized. Retrying payments initialization...");
                    
                    // Re-initialize payments after authorization
                    payments = await ysdk.getPayments({ signed: true });
                    
                    // Retry purchase
                    await payments.purchase({ id: purchaseId });
                    isAdsDisabled = true;
                    if (onPurchaseSuccessCallback) {
                        onPurchaseSuccessCallback();
                    }
                    alert("Реклама отключена! Спасибо за покупку.");
                } catch (authErr) {
                    console.error("Auth flow or purchase retry failed:", authErr);
                    alert("Не удалось завершить покупку после авторизации.");
                }
            }
        } else {
            alert("Покупка не была завершена: " + (err.message || err.code || "ошибка транзакции."));
        }
    }
}
