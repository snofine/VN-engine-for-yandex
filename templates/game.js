// game.js - Core Visual Novel Engine Player
let currentSceneId = "";
let currentDialogueIndex = 0;
let isMenuVisible = true;
let isGamePaused = false;

// Audio context or HTML5 Audio tracking (for future expansion or muting)
let isMuted = false;

// Monetization & Ad Timer variables
let lastAdTime = Date.now();
let adIntervalMs = 3 * 60 * 1000; // Default 3 minutes
let adsEnabled = false;
let removeAdsId = "";

// Initialize game on window load
window.addEventListener('DOMContentLoaded', () => {
    initEngine();
    window.addEventListener('resize', autoScaleGame);
});

// Initialize Engine
async function initEngine() {
    if (!window.storyData) {
        console.error("No story data found! Please make sure story.js is loaded.");
        document.getElementById('dialogue-text').innerText = "Ошибка: Данные истории не найдены (story.js отсутствует).";
        return;
    }

    const config = window.storyData.config || {};
    
    // Set game title
    document.title = config.title || "Моя Новелла";
    const hudTitle = document.getElementById('game-title');
    if (hudTitle) hudTitle.innerText = config.title || "Моя Новелла";
    
    const menuTitle = document.getElementById('menu-title-text');
    if (menuTitle) menuTitle.innerText = config.title || "Моя Новелла";

    // Setup monetization config
    if (config.ads_interval_minutes) {
        adIntervalMs = config.ads_interval_minutes * 60 * 1000;
        adsEnabled = true;
    }
    if (config.inapp_remove_ads_id) {
        removeAdsId = config.inapp_remove_ads_id;
    }

    // Setup GUI configurations
    if (window.storyData.gui) {
        const gui = window.storyData.gui;
        const root = document.documentElement;
        
        if (gui.panel_bg) root.style.setProperty('--panel-bg', gui.panel_bg);
        if (gui.panel_border) root.style.setProperty('--panel-border', gui.panel_border);
        if (gui.panel_radius !== undefined) root.style.setProperty('--panel-radius', gui.panel_radius + 'px');
        if (gui.dialogue_height !== undefined) root.style.setProperty('--dialogue-height', gui.dialogue_height + 'px');
        
        if (gui.text_color) root.style.setProperty('--text-color', gui.text_color);
        if (gui.text_size !== undefined) root.style.setProperty('--text-size', gui.text_size + 'px');
        
        if (gui.name_color) root.style.setProperty('--name-color', gui.name_color);
        if (gui.name_size !== undefined) root.style.setProperty('--name-size', gui.name_size + 'px');
        if (gui.name_bold !== undefined) root.style.setProperty('--name-bold', gui.name_bold ? 'bold' : 'normal');
        
        if (gui.choice_bg) root.style.setProperty('--choice-bg', gui.choice_bg);
        if (gui.choice_hover_bg) root.style.setProperty('--choice-hover-bg', gui.choice_hover_bg);
        if (gui.choice_border_color) root.style.setProperty('--choice-border-color', gui.choice_border_color);
        if (gui.choice_text_color) root.style.setProperty('--choice-text-color', gui.choice_text_color);
        if (gui.choice_size !== undefined) root.style.setProperty('--choice-size', gui.choice_size + 'px');
        
        if (gui.font_family) root.style.setProperty('--font-family', gui.font_family);
    }

    // Scale the game screen
    autoScaleGame();

    // Set Yandex SDK Callbacks
    onAdOpenCallback = () => {
        pauseGame();
    };
    
    onAdCloseCallback = (wasShown) => {
        resumeGame();
        lastAdTime = Date.now(); // Reset timer after showing ad
    };

    onPurchaseSuccessCallback = () => {
        // Hide remove ads buttons immediately
        const hudAdsBtn = document.getElementById('remove-ads-btn');
        if (hudAdsBtn) hudAdsBtn.style.display = 'none';
        
        const menuAdsBtn = document.getElementById('menu-remove-ads-btn');
        if (menuAdsBtn) menuAdsBtn.style.display = 'none';
        
        console.log("Ad removal purchase active.");
    };

    // Initialize SDK
    const sdkInitialized = await initYandexSDK(removeAdsId);
    
    // If IAP is enabled and we have an ID, show purchase buttons if ads are not yet disabled
    if (removeAdsId && !isAdsDisabled) {
        const hudAdsBtn = document.getElementById('remove-ads-btn');
        if (hudAdsBtn) hudAdsBtn.style.display = 'flex';
        
        const menuAdsBtn = document.getElementById('menu-remove-ads-btn');
        if (menuAdsBtn) menuAdsBtn.style.display = 'block';
    }

    // Start checking for ads interval
    startAdTimer();
}

// Start visual novel
function startGame() {
    isMenuVisible = false;
    const menuScreen = document.getElementById('menu-screen');
    menuScreen.style.opacity = '0';
    setTimeout(() => {
        menuScreen.style.display = 'none';
    }, 500);

    const config = window.storyData.config || {};
    const startScene = config.start_scene || Object.keys(window.storyData.scenes)[0];
    loadScene(startScene);
}

// Restart game
function restartGame() {
    const confirmRestart = confirm("Вы уверены, что хотите начать заново?");
    if (confirmRestart) {
        isMenuVisible = false;
        const menuScreen = document.getElementById('menu-screen');
        menuScreen.style.display = 'none';
        
        const config = window.storyData.config || {};
        const startScene = config.start_scene || Object.keys(window.storyData.scenes)[0];
        loadScene(startScene);
    }
}

// Load a specific scene by ID
function loadScene(sceneId) {
    const scenes = window.storyData.scenes;
    if (!scenes || !scenes[sceneId]) {
        console.error("Scene not found:", sceneId);
        return;
    }

    currentSceneId = sceneId;
    currentDialogueIndex = 0;
    
    const scene = scenes[sceneId];

    // 1. Set Background
    const bgLayer = document.getElementById('bg-layer');
    if (scene.background) {
        if (scene.background.startsWith('#') || scene.background.startsWith('rgba') || scene.background.startsWith('rgb')) {
            bgLayer.style.backgroundImage = 'none';
            bgLayer.style.backgroundColor = scene.background;
        } else {
            bgLayer.style.backgroundColor = 'transparent';
            bgLayer.style.backgroundImage = `url('${scene.background}')`;
        }
    } else {
        bgLayer.style.backgroundImage = 'none';
        bgLayer.style.backgroundColor = '#000';
    }

    // Hide choices at start of scene
    const choicesPanel = document.getElementById('choices-panel');
    choicesPanel.style.display = 'none';
    choicesPanel.innerHTML = '';

    // Show dialogue elements
    const uiLayer = document.getElementById('ui-layer');
    uiLayer.style.display = 'flex';

    // Present first dialogue step
    renderDialogueStep();
}

// Render dialogue step
function renderDialogueStep() {
    const scene = window.storyData.scenes[currentSceneId];
    if (!scene || !scene.dialogues || scene.dialogues.length === 0) {
        // No dialogues, check if choices or jump
        showSceneEndOptions();
        return;
    }

    const step = scene.dialogues[currentDialogueIndex];
    
    // Speaker name & Custom character color
    const speakerEl = document.getElementById('speaker-name');
    const textEl = document.getElementById('dialogue-text');
    
    // Reset styles
    speakerEl.style.color = '';
    textEl.style.fontStyle = 'normal';
    textEl.style.fontWeight = 'normal';

    if (step.is_thought) {
        // Thought: Hide speaker name, format text in parentheses & italics
        speakerEl.style.display = 'none';
        speakerEl.innerText = "";
        textEl.innerText = `(${step.text || ""})`;
        textEl.style.fontStyle = 'italic';
    } else {
        // Standard Dialogue
        const speakerName = step.speaker || "";
        speakerEl.innerText = speakerName;
        
        if (!speakerName) {
            speakerEl.style.display = 'none';
        } else {
            speakerEl.style.display = 'block';
            // Apply custom speaker color if defined in character configuration
            if (step.character_id && window.storyData.config && window.storyData.config.characters) {
                const charInfo = window.storyData.config.characters[step.character_id];
                if (charInfo && charInfo.color) {
                    speakerEl.style.color = charInfo.color;
                }
            }
        }
        
        textEl.innerText = step.text || "";
        
        // Apply inline text formatting flags
        if (step.text_italic) {
            textEl.style.fontStyle = 'italic';
        }
        if (step.text_bold) {
            textEl.style.fontWeight = 'bold';
        }
    }

    // Sprites display
    const spriteSlots = {
        'left': document.getElementById('sprite-left'),
        'center': document.getElementById('sprite-center'),
        'right': document.getElementById('sprite-right')
    };

    // If step contains a sprite setting, adjust that position.
    // We also support clearing sprites.
    if (step.sprite) {
        let pos = step.sprite.position;
        if (pos === undefined || pos === null) pos = 'center';
        const imgUrl = step.sprite.image || '';
        
        // Find which slot to use and set its horizontal and vertical positions
        let slotName = 'center';
        let leftValue = '';
        let bottomValue = '0%';
        
        if (Array.isArray(pos)) {
            const x = parseFloat(pos[0] !== undefined ? pos[0] : 50);
            const y = parseFloat(pos[1] !== undefined ? pos[1] : 0);
            leftValue = x + '%';
            bottomValue = y + '%';
            
            // Map X coordinate to slot
            if (x < 35) slotName = 'left';
            else if (x > 65) slotName = 'right';
            else slotName = 'center';
        } else if (typeof pos === 'number' || (typeof pos === 'string' && pos.trim() !== '' && !isNaN(pos))) {
            const numericPos = parseFloat(pos);
            leftValue = numericPos + '%';
            bottomValue = '0%';
            
            if (numericPos < 35) slotName = 'left';
            else if (numericPos > 65) slotName = 'right';
            else slotName = 'center';
        } else {
            // Preset values
            slotName = pos.toString().toLowerCase();
            bottomValue = '0%';
            if (slotName === 'left') {
                leftValue = '25%';
            } else if (slotName === 'right') {
                leftValue = '75%';
            } else {
                slotName = 'center';
                leftValue = '50%';
            }
        }
        
        const targetSlot = spriteSlots[slotName];
        if (targetSlot) {
            if (imgUrl) {
                targetSlot.src = imgUrl;
                targetSlot.style.left = leftValue;
                targetSlot.style.bottom = bottomValue;
                targetSlot.classList.add('active');
            } else {
                targetSlot.classList.remove('active');
                setTimeout(() => { targetSlot.src = ''; }, 300);
            }
        }
    }

    // Update indicator
    const indicator = document.getElementById('next-indicator');
    if (currentDialogueIndex < scene.dialogues.length - 1) {
        indicator.innerText = "▶";
    } else {
        // If it's the last dialogue, change indicator or hide
        if (scene.choices && scene.choices.length > 0) {
            indicator.innerText = "❓";
        } else {
            indicator.innerText = "■";
        }
    }
}

// Dialogue panel clicked
function onDialogueClick() {
    if (isGamePaused || isMenuVisible) return;

    const scene = window.storyData.scenes[currentSceneId];
    if (!scene) return;

    if (currentDialogueIndex < scene.dialogues.length - 1) {
        currentDialogueIndex++;
        renderDialogueStep();
    } else {
        showSceneEndOptions();
    }
}

// Show choices or move to target scene if specified
function showSceneEndOptions() {
    const scene = window.storyData.scenes[currentSceneId];
    if (!scene) return;

    // Hide dialogue panel so user is forced to make a choice
    const uiLayer = document.getElementById('ui-layer');
    
    if (scene.choices && scene.choices.length > 0) {
        uiLayer.style.display = 'none'; // Hide dialogue panel
        
        const choicesPanel = document.getElementById('choices-panel');
        choicesPanel.innerHTML = '';
        choicesPanel.style.display = 'flex';

        scene.choices.forEach(choice => {
            const btn = document.createElement('div');
            btn.className = 'choice-btn';
            btn.innerText = choice.text;
            btn.onclick = () => {
                // Check ads timer before loading next scene
                checkAndTriggerAd(() => {
                    loadScene(choice.next_scene);
                });
            };
            choicesPanel.appendChild(btn);
        });
    } else if (scene.next_scene) {
        // Automatic jump to next scene
        checkAndTriggerAd(() => {
            loadScene(scene.next_scene);
        });
    } else {
        // End of game
        uiLayer.style.display = 'none';
        const choicesPanel = document.getElementById('choices-panel');
        choicesPanel.innerHTML = `
            <div style="text-align:center; color: #fff; margin-bottom: 20px;">Конец Истории</div>
            <div class="choice-btn" onclick="restartGame()">🔄 Играть заново</div>
        `;
        choicesPanel.style.display = 'flex';
    }
}

// Purchase function called from HUD
function purchaseAdsRemoval() {
    if (removeAdsId) {
        purchaseRemoveAds(removeAdsId);
    } else {
        alert("Внутриигровые покупки не настроены в этом проекте.");
    }
}

// Monetization Timer checking in background
function startAdTimer() {
    if (!adsEnabled) return;
    
    setInterval(() => {
        // If ads are disabled by payment, do nothing
        if (isAdsDisabled) return;

        const elapsed = Date.now() - lastAdTime;
        if (elapsed >= adIntervalMs) {
            console.log("Ads interval reached. Ready to show advertisement on next transition.");
        }
    }, 1000);
}

// Check and trigger advertisement on scene transitions or choice selections
function checkAndTriggerAd(onCompleteCallback) {
    if (!adsEnabled || isAdsDisabled) {
        onCompleteCallback();
        return;
    }

    const elapsed = Date.now() - lastAdTime;
    if (elapsed >= adIntervalMs) {
        // Pause game logic
        pauseGame();
        
        // Show advertisement
        // Once ad closes (or errors), resumeGame is triggered, resetting timer, and then we continue the transition
        onAdCloseCallback = (wasShown) => {
            resumeGame();
            lastAdTime = Date.now();
            onCompleteCallback();
        };
        
        showFullscreenAd();
    } else {
        // If interval is not yet reached, continue immediately
        onCompleteCallback();
    }
}

// Pause game interaction
function pauseGame() {
    isGamePaused = true;
    const pauseEl = document.getElementById('pause-overlay');
    if (pauseEl) pauseEl.style.display = 'flex';
    
    // Mute any sound if context exists (HTML5 Audio integration helper)
    muteAllAudio(true);
}

// Resume game interaction
function resumeGame() {
    isGamePaused = false;
    const pauseEl = document.getElementById('pause-overlay');
    if (pauseEl) pauseEl.style.display = 'none';
    
    // Unmute sound
    muteAllAudio(false);
}

// Sound mute/unmute
function muteAllAudio(shouldMute) {
    isMuted = shouldMute;
    // Mute all HTML5 Audio and Video elements
    const mediaElements = document.querySelectorAll('audio, video');
    mediaElements.forEach(media => {
        media.muted = shouldMute;
    });
    
    // Support Web Audio API contexts if defined in the global window object
    if (window.audioContext) {
        if (shouldMute && window.audioContext.state === 'running') {
            window.audioContext.suspend();
        } else if (!shouldMute && window.audioContext.state === 'suspended') {
            window.audioContext.resume();
        }
    }
    console.log(shouldMute ? "Audio Muted." : "Audio Unmuted.");
}

// Adaptive scale function to make it work on mobile and different resolutions
function autoScaleGame() {
    const container = document.getElementById('game-container');
    if (!container) return;

    const baseWidth = 1280;
    const baseHeight = 720;
    
    const windowWidth = window.innerWidth;
    const windowHeight = window.innerHeight;
    
    const scaleX = windowWidth / baseWidth;
    const scaleY = windowHeight / baseHeight;
    const scale = Math.min(scaleX, scaleY);
    
    container.style.transform = `scale(${scale})`;
    
    // Position container correctly in center
    container.style.position = 'absolute';
    container.style.left = `${(windowWidth - baseWidth * scale) / 2}px`;
    container.style.top = `${(windowHeight - baseHeight * scale) / 2}px`;
}
