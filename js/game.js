const Game = {
    isRunning: false,
    startTime: null,
    survivalTime: 0,
    timerInterval: null,

    init() {
        this.setupEventListeners();
    },

    setupEventListeners() {
        document.getElementById('start-btn').addEventListener('click', () => this.startGame());
        document.getElementById('restart-btn').addEventListener('click', () => this.restartGame());
    },

    startGame() {
        this.isRunning = true;
        this.startTime = Date.now();
        this.survivalTime = 0;
        RuleSystem.reset();
        SceneSystem.reset();
        AnomalySystem.reset();

        UI.hideScreen('start-screen');
        UI.showHeader();
        UI.showMainContent();

        const firstRule = RuleSystem.generateRule();
        UI.addRule(firstRule);

        SceneSystem.setCurrentScene('entrance');
        UI.displayScene(SceneSystem.getCurrentScene());

        this.startTimer();
    },

    restartGame() {
        this.stopTimer();
        UI.hideScreen('game-over-screen');
        this.startGame();
    },

    startTimer() {
        this.timerInterval = setInterval(() => {
            this.survivalTime = Math.floor((Date.now() - this.startTime) / 1000 / 60);
            UI.updateStats(this.survivalTime, AnomalySystem.anomalyCount);
        }, 1000);
    },

    stopTimer() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
    },

    handleChoice(choiceIndex) {
        if (!this.isRunning) return;

        const shouldAddRule = SceneSystem.shouldAddRule(choiceIndex);
        const nextSceneId = SceneSystem.getNextScene(choiceIndex);

        if (shouldAddRule && Math.random() > 0.3) {
            const newRule = RuleSystem.generateRule();
            UI.addRule(newRule);

            const overriddenRule = RuleSystem.overrideOldRules();
            if (overriddenRule) {
                UI.updateRules();
            }
        }

        const violatedRule = RuleSystem.checkRuleViolation('choice', {
            scene: SceneSystem.getCurrentScene().id,
            choice: choiceIndex
        });

        if (violatedRule) {
            const anomaly = AnomalySystem.triggerAnomaly(violatedRule);
            UI.triggerAnomalyEffect(anomaly);
            
            if (anomaly.isGameOver) {
                this.gameOver(anomaly);
                return;
            }
        }

        if (nextSceneId === 'anomaly_scene') {
            const anomaly = AnomalySystem.triggerAnomaly(null);
            UI.displayAnomalyScene(anomaly);
            
            if (anomaly.isGameOver) {
                this.gameOver(anomaly);
                return;
            }
        } else {
            SceneSystem.setCurrentScene(nextSceneId);
            UI.displayScene(SceneSystem.getCurrentScene());
        }

        UI.updateStats(this.survivalTime, AnomalySystem.anomalyCount);
    },

    gameOver(anomaly) {
        this.isRunning = false;
        this.stopTimer();

        UI.hideMainContent();
        UI.hideHeader();
        UI.showGameOverScreen({
            time: this.survivalTime,
            rules: RuleSystem.rules.length,
            anomalies: AnomalySystem.anomalyCount,
            reason: AnomalySystem.getGameOverReason()
        });
    }
};

document.addEventListener('DOMContentLoaded', () => {
    Game.init();
});
