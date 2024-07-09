<template>
  <div class="container">
    <h1>随机小游戏设置</h1>
    <button @click="setRandomGame">点我随机一个小游戏</button>

    <div v-if="selectedGame">
      <h2>当前小游戏：</h2>
      <p>{{ selectedGame.name }}</p>
      <p>{{ selectedGame.description }}</p>

      <div v-if="selectedGame.name === '猜数字'">
        <h3>猜数字游戏</h3>
        <p>请猜一个在1到100之间的随机数字。</p>
        <input v-model.number="guess" type="number" placeholder="输入你的猜测" />
        <button @click="checkGuess">检查猜测</button>
        <p v-if="result">{{ result }}</p>
      </div>

      <div v-if="selectedGame.name === '石头剪刀布'">
        <h3>石头剪刀布游戏</h3>
        <p>选择一个：石头、剪刀或布</p>
        <button @click="playGame('石头')">石头</button>
        <button @click="playGame('剪刀')">剪刀</button>
        <button @click="playGame('布')">布</button>
        <p v-if="gameResult">{{ gameResult }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      games: [
        { name: '猜数字', description: '猜一个在1到100之间的随机数字。' },
        { name: '石头剪刀布', description: '与计算机进行石头剪刀布游戏。' },
      ],
      selectedGame: null,
      guess: null,
      result: null,
      gameResult: null,
    };
  },
  methods: {
    setRandomGame() {
      const randomIndex = Math.floor(Math.random() * this.games.length);
      this.selectedGame = this.games[randomIndex];
      this.resetGame(); // 重置游戏相关状态
    },
    resetGame() {
      this.guess = null;
      this.result = null;
      this.gameResult = null;
    },
    checkGuess() {
      const randomNumber = Math.floor(Math.random() * 100) + 1;
      if (this.guess === randomNumber) {
        this.result = '恭喜，你猜对了!';
      } else {
        this.result = '很遗憾，再试一次吧。';
      }
    },
    playGame(userChoice) {
      const choices = ['石头', '剪刀', '布'];
      const computerChoice = choices[Math.floor(Math.random() * 3)];

      if (userChoice === computerChoice) {
        this.gameResult = '平局，再试一次。';
      } else if (
        (userChoice === '石头' && computerChoice === '剪刀') ||
        (userChoice === '剪刀' && computerChoice === '布') ||
        (userChoice === '布' && computerChoice === '石头')
      ) {
        this.gameResult = '恭喜，你赢了!';
      } else {
        this.gameResult = '很遗憾，你输了。再试一次吧。';
      }
    },
  },
};
</script>

<style scoped>
.container {
  text-align: center;
  padding: 20px;
}

button {
  font-size: 16px;
  padding: 10px;
  margin-top: 20px;
  cursor: pointer;
}

h1, h2, h3 {
  color: #333;
  margin-bottom: 10px;
}

p {
  margin: 10px 0;
}
</style>
