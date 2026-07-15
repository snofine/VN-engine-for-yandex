// game.js - Core Visual Novel Engine Player (Polished)
let currentSceneId = "";
let currentDialogueIndex = 0;
let isMenuVisible = true;
let isGamePaused = false;

// Audio context or HTML5 Audio tracking
let isMuted = false;
let bgmAudio = null;
let currentBgmPath = "";
let bgmVolume = 1.0;

// Monetization & Ad Timer variables
let lastAdTime = Date.now();
let adIntervalMs = 3 * 60 * 1000; // Default 3 minutes
let adsEnabled = false;
let removeAdsId = "";

// Typewriter effect state
let typewriterTimer = null;
let typewriterFullHTML = "";
let isTypewriterActive = false;
const TYPEWRITER_SPEED = 30; // ms per character

// Initialize game on window load
window.addEventListener('DOMContentLoaded', () => {
    initEngine();
    window.addEventListener('resize', autoScaleGame);
    
    // Keyboard support
    window.addEventListener('keydown', handleKeyPress);
});

// Keyboard handler
function handleKeyPress(e) {
    if (isMenuVisible || isGamePaused) return;
    
    if (e.code === 'Space' || e.code === 'Enter') {
        e.preventDefault();
        onDialogueClick();
    }
    
    // Number keys 1-9 to select choices
    if (e.code.startsWith('Digit') && e.code !== 'Digit0') {
        const choicesPanel = document.getElementById('choices-panel');
        if (choicesPanel && choicesPanel.style.display !== 'none') {
            const num = parseInt(e.code.replace('Digit', ''));
            const buttons = choicesPanel.querySelectorAll('.choice-btn');
            if (num <= buttons.length) {
                buttons[num - 1].click();
            }
        }
    }
}

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

    // Volume slider setup
    const volumeSlider = document.getElementById('volume-slider');
    if (volumeSlider) {
        volumeSlider.addEventListener('input', (e) => {
            bgmVolume = parseInt(e.target.value) / 100;
            if (bgmAudio) bgmAudio.volume = bgmVolume;
        });
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

    // Hide loading screen
    const loadingScreen = document.getElementById('loading-screen');
    if (loadingScreen) {
        loadingScreen.classList.add('ready');
        setTimeout(() => { loadingScreen.style.display = 'none'; }, 600);
    }

    // Saves disabled
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
    const startScene = config.start_scene || Object.keys(window.storyData.scenes || {})[0];
    if (startScene) {
        loadScene(startScene);
    } else {
        console.error("No scenes found in story data.");
    }
}

// Restart game
function restartGame() {
    if (!confirm("Вы уверены, что хотите начать заново?")) return;
    
    isMenuVisible = false;
    const menuScreen = document.getElementById('menu-screen');
    menuScreen.style.display = 'none';
    
    const config = window.storyData.config || {};
    const startScene = config.start_scene || Object.keys(window.storyData.scenes || {})[0];
    if (startScene) loadScene(startScene);
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

    // 1. Set Background with transition effects
    const bgLayer = document.getElementById('bg-layer');
    const transType = scene.transition || 'none';
    let transClass = '';
    
    if (transType === 'fade') transClass = 'transition-fade-out';
    else if (transType === 'slide') transClass = 'transition-slide-out';
    else if (transType === 'zoom') transClass = 'transition-zoom-out';

    const updateBgGraphic = () => {
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
    };

    if (transClass) {
        bgLayer.classList.add(transClass);
        setTimeout(() => {
            updateBgGraphic();
            bgLayer.classList.remove(transClass);
        }, 250);
    } else {
        updateBgGraphic();
    }

    // 2. Play Background Music (BGM) with crossfade
    if (scene.bgm) {
        if (scene.bgm === 'stop') {
            fadeOutBGM();
            currentBgmPath = "";
        } else if (scene.bgm !== currentBgmPath) {
            fadeOutBGM(() => {
                currentBgmPath = scene.bgm;
                bgmAudio = new Audio(scene.bgm);
                bgmAudio.loop = true;
                bgmAudio.volume = 0;
                bgmAudio.muted = isMuted;
                bgmAudio.play().catch(e => console.log("BGM playback blocked:", e));
                fadeInBGM();
            });
        }
    }

    // Clear all sprites for fresh scene
    ['sprite-left', 'sprite-center', 'sprite-right'].forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.classList.remove('active');
            setTimeout(() => { el.src = ''; }, 300);
        }
    });

    // Hide choices at start of scene
    const choicesPanel = document.getElementById('choices-panel');
    choicesPanel.style.display = 'none';
    choicesPanel.innerHTML = '';

    // Show dialogue elements
    const uiLayer = document.getElementById('ui-layer');
    uiLayer.style.display = 'flex';

    // Present first dialogue step
    renderDialogueStep();
    
    // Progress auto-save disabled
}

// BGM crossfade helpers
function fadeOutBGM(onComplete) {
    if (!bgmAudio) {
        if (onComplete) onComplete();
        return;
    }
    const fadeStep = 0.05;
    const fadeInterval = setInterval(() => {
        if (bgmAudio && bgmAudio.volume > fadeStep) {
            bgmAudio.volume = Math.max(0, bgmAudio.volume - fadeStep);
        } else {
            clearInterval(fadeInterval);
            if (bgmAudio) {
                bgmAudio.pause();
                bgmAudio = null;
            }
            if (onComplete) onComplete();
        }
    }, 30);
}

function fadeInBGM() {
    if (!bgmAudio) return;
    const targetVolume = bgmVolume;
    const fadeStep = 0.05;
    const fadeInterval = setInterval(() => {
        if (bgmAudio && bgmAudio.volume < targetVolume - fadeStep) {
            bgmAudio.volume = Math.min(targetVolume, bgmAudio.volume + fadeStep);
        } else {
            clearInterval(fadeInterval);
            if (bgmAudio) bgmAudio.volume = targetVolume;
        }
    }, 30);
}

// Parse formatting tags and format dialogue text dynamically
function parseDialogueText(text) {
    if (!text) return "";
    
    // First, escape all HTML tags to prevent execution of untrusted scripts/frames
    let escaped = text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
        
    // 1. Support standard HTML/XML tags by restoring them from escaped state:
    escaped = escaped.replace(/&lt;b&gt;(.*?)&lt;\/b&gt;/gsi, "<b>$1</b>");
    escaped = escaped.replace(/&lt;i&gt;(.*?)&lt;\/i&gt;/gsi, "<i>$1</i>");
    escaped = escaped.replace(/&lt;u&gt;(.*?)&lt;\/u&gt;/gsi, "<u>$1</u>");
    escaped = escaped.replace(/&lt;s&gt;(.*?)&lt;\/s&gt;/gsi, "<s>$1</s>");
    
    // Custom tags in HTML format:
    // <shake>text</shake> -> <span class="shake-text">text</span>
    escaped = escaped.replace(/&lt;shake&gt;(.*?)&lt;\/shake&gt;/gsi, '<span class="shake-text">$1</span>');
    // <color=red>text</color> -> <span style="color: $1">$2</span>
    escaped = escaped.replace(/&lt;color=([\w#]+)&gt;(.*?)&lt;\/color&gt;/gsi, '<span style="color: $1">$2</span>');
    // <color color="red">text</color> -> <span style="color: $1">$2</span>
    escaped = escaped.replace(/&lt;color\s+color="([\w#]+)"&gt;(.*?)&lt;\/color&gt;/gsi, '<span style="color: $1">$2</span>');
    escaped = escaped.replace(/&lt;color\s+color='([\w#]+)'&gt;(.*?)&lt;\/color&gt;/gsi, '<span style="color: $1">$2</span>');

    // 2. Keep backward compatibility with slash tags:
    escaped = escaped.replace(/\/b\/(.*?)\/b\//gsi, "<b>$1</b>");
    escaped = escaped.replace(/\/i\/(.*?)\/i\//gsi, "<i>$1</i>");
    escaped = escaped.replace(/\/u\/(.*?)\/u\//gsi, "<u>$1</u>");
    escaped = escaped.replace(/\/s\/(.*?)\/s\//gsi, "<s>$1</s>");
    escaped = escaped.replace(/\/shake\/(.*?)\/shake\//gsi, '<span class="shake-text">$1</span>');
    escaped = escaped.replace(/\/color=([\w#]+)\/(.*?)\/color\//gsi, '<span style="color: $1">$2</span>');
    
    return escaped;
}

// Typewriter effect: reveal text character by character
function startTypewriter(element, html) {
    stopTypewriter();
    typewriterFullHTML = html;
    isTypewriterActive = true;
    element.classList.add('typewriter-active');
    
    // Parse HTML to extract plain text length for timing
    const temp = document.createElement('div');
    temp.innerHTML = html;
    const plainText = temp.textContent || temp.innerText;
    const totalChars = plainText.length;
    
    if (totalChars === 0) {
        element.innerHTML = html;
        isTypewriterActive = false;
        element.classList.remove('typewriter-active');
        return;
    }
    
    let charIndex = 0;
    
    // We reveal by wrapping content in a span and using CSS to clip
    // Simpler approach: add chars one by one from plain text while preserving tags
    element.innerHTML = '';
    
    typewriterTimer = setInterval(() => {
        charIndex++;
        if (charIndex >= totalChars) {
            clearInterval(typewriterTimer);
            typewriterTimer = null;
            element.innerHTML = html;
            isTypewriterActive = false;
            element.classList.remove('typewriter-active');
        } else {
            // Show partial text by truncating plain text and re-applying tags
            element.innerHTML = truncateHTMLByChars(html, charIndex);
        }
    }, TYPEWRITER_SPEED);
}

// Truncate HTML string to show only N visible characters
function truncateHTMLByChars(html, maxChars) {
    let result = '';
    let visibleCount = 0;
    let inTag = false;
    let tagBuffer = '';
    const openTags = [];
    
    for (let i = 0; i < html.length; i++) {
        const ch = html[i];
        
        if (ch === '<') {
            inTag = true;
            tagBuffer = '<';
            continue;
        }
        
        if (inTag) {
            tagBuffer += ch;
            if (ch === '>') {
                inTag = false;
                result += tagBuffer;
                // Track open/close tags
                const closingMatch = tagBuffer.match(/^<\/(\w+)>/);
                const openMatch = tagBuffer.match(/^<(\w+)/);
                if (closingMatch && openTags.length > 0 && openTags[openTags.length - 1] === closingMatch[1]) {
                    openTags.pop();
                } else if (openMatch && !tagBuffer.match(/\/\s*>$/) && !closingMatch) {
                    openTags.push(openMatch[1]);
                }
                tagBuffer = '';
            }
            continue;
        }
        
        if (visibleCount < maxChars) {
            result += ch;
            visibleCount++;
        } else {
            break;
        }
    }
    
    // Close any open tags
    for (let j = openTags.length - 1; j >= 0; j--) {
        result += `</${openTags[j]}>`;
    }
    
    return result;
}

function stopTypewriter() {
    if (typewriterTimer) {
        clearInterval(typewriterTimer);
        typewriterTimer = null;
    }
    isTypewriterActive = false;
    const textEl = document.getElementById('dialogue-text');
    if (textEl) textEl.classList.remove('typewriter-active');
}

function skipTypewriter() {
    if (isTypewriterActive) {
        stopTypewriter();
        const textEl = document.getElementById('dialogue-text');
        if (textEl) textEl.innerHTML = typewriterFullHTML;
        return true; // Indicate we consumed the click
    }
    return false;
}

// Render dialogue step
function renderDialogueStep() {
    const scene = window.storyData.scenes[currentSceneId];
    if (!scene || !scene.dialogues || scene.dialogues.length === 0) {
        showSceneEndOptions();
        return;
    }

    const step = scene.dialogues[currentDialogueIndex];
    if (!step) {
        showSceneEndOptions();
        return;
    }
    
    // Play sound effect (SFX) if specified in dialogue step
    if (step.sfx) {
        const sfx = new Audio(step.sfx);
        sfx.muted = isMuted;
        sfx.play().catch(e => console.log("SFX playback blocked or failed:", e));
    }
    
    // Speaker name & Custom character color
    const speakerEl = document.getElementById('speaker-name');
    const textEl = document.getElementById('dialogue-text');
    
    // Reset styles
    speakerEl.style.color = '';
    textEl.style.fontStyle = 'normal';
    textEl.style.fontWeight = 'normal';

    let formattedText = '';

    if (step.is_thought) {
        // Thought: Hide speaker name, format text in parentheses & italics
        speakerEl.style.display = 'none';
        speakerEl.innerText = "";
        formattedText = `(${parseDialogueText(step.text || "")})`;
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
        
        formattedText = parseDialogueText(step.text || "");
        
        // Apply inline text formatting flags
        if (step.text_italic) {
            textEl.style.fontStyle = 'italic';
        }
        if (step.text_bold) {
            textEl.style.fontWeight = 'bold';
        }
    }

    // Start typewriter effect
    startTypewriter(textEl, formattedText);

    // Sprites display
    const spriteSlots = {
        'left': document.getElementById('sprite-left'),
        'center': document.getElementById('sprite-center'),
        'right': document.getElementById('sprite-right')
    };

    if (step.sprite) {
        let pos = step.sprite.position;
        if (pos === undefined || pos === null) pos = 'center';
        const imgUrl = step.sprite.image || '';
        
        let slotName = 'center';
        let leftValue = '';
        let bottomValue = '0%';
        
        if (Array.isArray(pos)) {
            const x = parseFloat(pos[0] !== undefined ? pos[0] : 50);
            const y = parseFloat(pos[1] !== undefined ? pos[1] : 0);
            leftValue = x + '%';
            bottomValue = y + '%';
            
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

    // If typewriter is still running, skip to full text first
    if (skipTypewriter()) return;

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

        scene.choices.forEach((choice, index) => {
            const btn = document.createElement('div');
            btn.className = 'choice-btn';
            btn.style.setProperty('--choice-delay', `${index * 0.1}s`);
            btn.innerText = `${index + 1}. ${choice.text}`;
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
        stopTypewriter();
        uiLayer.style.display = 'none';
        const choicesPanel = document.getElementById('choices-panel');
        choicesPanel.innerHTML = `
            <div class="end-screen">
                <div class="end-screen-title">Конец Истории</div>
                <div class="end-screen-subtitle">Спасибо за прохождение!</div>
            </div>
            <div class="choice-btn" style="--choice-delay: 0.3s" onclick="restartGame()">🔄 Играть заново</div>
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
        const originalCallback = onAdCloseCallback;
        onAdCloseCallback = (wasShown) => {
            resumeGame();
            lastAdTime = Date.now();
            onAdCloseCallback = originalCallback; // Restore
            onCompleteCallback();
        };
        
        showFullscreenAd();
    } else {
        onCompleteCallback();
    }
}

// Pause game interaction
function pauseGame() {
    isGamePaused = true;
    const pauseEl = document.getElementById('pause-overlay');
    if (pauseEl) pauseEl.style.display = 'flex';
    
    // Mute any sound if context exists
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
    
    // Mute our active background music
    if (bgmAudio) {
        bgmAudio.muted = shouldMute;
    }
    
    // Mute all other HTML5 Audio and Video elements
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
}

// Saves disabled

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
