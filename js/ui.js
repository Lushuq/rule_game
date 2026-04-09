const UI = {
    elements: {},

    init() {
        this.cacheElements();
    },

    cacheElements() {
        this.elements = {
            header: document.getElementById('header'),
            mainContent: document.getElementById('main-content'),
            sceneTitle: document.getElementById('scene-title'),
            sceneDescription: document.getElementById('scene-description'),
            sceneChoices: document.getElementById('scene-choices'),
            rulesList: document.getElementById('rules-list'),
            survivalTime: document.getElementById('survival-time'),
            anomalyCount: document.getElementById('anomaly-count'),
            startScreen: document.getElementById('start-screen'),
            gameOverScreen: document.getElementById('game-over-screen'),
            gameOverTitle: document.getElementById('game-over-title'),
            gameOverMessage: document.getElementById('game-over-message'),
            finalTime: document.getElementById('final-time'),
            finalRules: document.getElementById('final-rules'),
            finalAnomalies: document.getElementById('final-anomalies'),
            anomalyOverlay: document.getElementById('anomaly-overlay')
        };
    },

    showHeader() {
        this.elements.header.style.display = 'flex';
    },

    hideHeader() {
        this.elements.header.style.display = 'none';
    },

    showMainContent() {
        this.elements.mainContent.style.display = 'flex';
    },

    hideMainContent() {
        this.elements.mainContent.style.display = 'none';
    },

    showScreen(screenId) {
        const screen = document.getElementById(screenId);
        if (screen) {
            screen.classList.add('active');
        }
    },

    hideScreen(screenId) {
        const screen = document.getElementById(screenId);
        if (screen) {
            screen.classList.remove('active');
        }
    },

    displayScene(scene) {
        this.elements.sceneTitle.textContent = scene.title;
        this.elements.sceneTitle.classList.add('fade-in');
        setTimeout(() => this.elements.sceneTitle.classList.remove('fade-in'), 500);

        this.elements.sceneDescription.textContent = scene.description;
        this.elements.sceneDescription.classList.add('fade-in');
        setTimeout(() => this.elements.sceneDescription.classList.remove('fade-in'), 500);

        this.elements.sceneChoices.innerHTML = '';
        scene.choices.forEach((choice, index) => {
            const btn = document.createElement('button');
            btn.className = 'choice-btn fade-in';
            btn.textContent = choice.text;
            btn.addEventListener('click', () => Game.handleChoice(index));
            this.elements.sceneChoices.appendChild(btn);
        });
    },

    displayAnomalyScene(anomaly) {
        this.elements.sceneTitle.textContent = anomaly.title;
        this.elements.sceneDescription.textContent = anomaly.description;
        
        this.elements.sceneChoices.innerHTML = '';
        const btn = document.createElement('button');
        btn.className = 'choice-btn fade-in';
        btn.textContent = '继续...';
        btn.addEventListener('click', () => {
            SceneSystem.setCurrentScene('lobby');
            this.displayScene(SceneSystem.getCurrentScene());
        });
        this.elements.sceneChoices.appendChild(btn);
    },

    addRule(rule) {
        this.updateRules();
        this.highlightNewRule();
    },

    updateRules() {
        this.elements.rulesList.innerHTML = '';
        const rules = RuleSystem.rules;
        
        rules.forEach(rule => {
            const ruleEl = document.createElement('div');
            ruleEl.className = 'rule-item';
            ruleEl.id = `rule-${rule.id}`;
            
            if (rule.status === 'overridden') {
                ruleEl.classList.add('overridden');
            } else if (rule.contradicts.length > 0) {
                ruleEl.classList.add('contradicting');
            }

            let html = `<span class="rule-number">#${rule.id}</span>${rule.text}`;
            
            if (rule.contradicts.length > 0 && rule.status !== 'overridden') {
                html += `<span class="rule-status">⚠️ 与规则 #${rule.contradicts.join(', #')} 矛盾</span>`;
            }
            
            if (rule.status === 'overridden') {
                html += `<span class="rule-status">❌ 已被规则 #${rule.overriddenBy} 取代</span>`;
            }

            ruleEl.innerHTML = html;
            this.elements.rulesList.appendChild(ruleEl);
        });
    },

    highlightNewRule() {
        const rules = this.elements.rulesList.children;
        if (rules.length > 0) {
            const lastRule = rules[rules.length - 1];
            lastRule.style.animation = 'pulse 1s ease';
            setTimeout(() => {
                lastRule.style.animation = '';
            }, 1000);
        }
    },

    updateStats(time, anomalies) {
        this.elements.survivalTime.textContent = time;
        this.elements.anomalyCount.textContent = anomalies;
    },

    triggerAnomalyEffect(anomaly) {
        this.elements.anomalyOverlay.classList.add('active');
        
        this.elements.sceneTitle.classList.add('text-glitch');
        this.elements.sceneDescription.classList.add('text-glitch');

        switch (anomaly.effect) {
            case 'glitch':
                this.applyGlitchEffect();
                break;
            case 'flicker':
                this.applyFlickerEffect();
                break;
            case 'shake':
                this.applyShakeEffect();
                break;
            case 'distortion':
                this.applyDistortionEffect();
                break;
            case 'darkness':
                this.applyDarknessEffect();
                break;
        }

        setTimeout(() => {
            this.elements.anomalyOverlay.classList.remove('active');
            this.elements.sceneTitle.classList.remove('text-glitch');
            this.elements.sceneDescription.classList.remove('text-glitch');
            this.removeEffects();
        }, 2000);
    },

    applyGlitchEffect() {
        document.body.style.filter = 'hue-rotate(90deg)';
    },

    applyFlickerEffect() {
        let flickerCount = 0;
        const flickerInterval = setInterval(() => {
            document.body.style.opacity = flickerCount % 2 === 0 ? '0.3' : '1';
            flickerCount++;
            if (flickerCount > 10) {
                clearInterval(flickerInterval);
                document.body.style.opacity = '1';
            }
        }, 100);
    },

    applyShakeEffect() {
        let shakeCount = 0;
        const shakeInterval = setInterval(() => {
            const x = (Math.random() - 0.5) * 20;
            const y = (Math.random() - 0.5) * 20;
            document.body.style.transform = `translate(${x}px, ${y}px)`;
            shakeCount++;
            if (shakeCount > 20) {
                clearInterval(shakeInterval);
                document.body.style.transform = '';
            }
        }, 50);
    },

    applyDistortionEffect() {
        document.body.style.filter = 'blur(2px) contrast(2)';
    },

    applyDarknessEffect() {
        document.body.style.filter = 'brightness(0.1)';
    },

    removeEffects() {
        document.body.style.filter = '';
        document.body.style.transform = '';
    },

    showGameOverScreen(stats) {
        this.elements.gameOverTitle.textContent = '游戏结束';
        this.elements.gameOverMessage.textContent = stats.reason;
        this.elements.finalTime.textContent = stats.time;
        this.elements.finalRules.textContent = stats.rules;
        this.elements.finalAnomalies.textContent = stats.anomalies;
        
        this.showScreen('game-over-screen');
    }
};

UI.init();
