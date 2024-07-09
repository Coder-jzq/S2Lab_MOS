<template>
  <div class="container">
    <div class="header">语音MOS打分</div>
    
    <div style="padding: 20px; background-color: aliceblue;"></div>
    
    <div class="table">
      <div
        v-for="(data, tableIndex) in tableDatas"
        :key="tableIndex"
        style="background-color: #f5f5f5; margin-bottom: 10px;"
      >
        <div style="text-align: center; display: flex;" class="cell">
          <div style="width: 20%;">文件：</div>
          <div style="width: 80%; text-align: left;">{{ data.text }}</div>
        </div>
        <div class="row header-row">
          <text class="cell">model</text>
          <text class="cell">audio</text>
          <text class="cell">流畅度分数</text>
          <text class="cell">重音感知分数</text>
        </div>
        <div v-for="(row, rowIndex) in data.tableData" :key="rowIndex" class="row">
          <text class="cell">{{ row.model }}</text>
          <audio :src="row.audio" controls></audio>
          <input
            class="cell"
            @focus="clearInput(row, 'scores1')"
            style="background-color: antiquewhite;"
            v-model="row.scores1"
            type="number"
            placeholder="流畅度"
          />
          <input
            class="cell"
            @focus="clearInput(row, 'scores2')"
            style="background-color: darkcyan;"
            v-model="row.scores2"
            type="number"
            placeholder="重音"
          />
        </div>
      </div>
    </div>
    
    <div class="export-btn" @click="exportToJson">导出JSON</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tableDatas: [],
    };
  },
  mounted() {
    this.loadAudioFiles();
    this.detectDevice();
  },
  methods: {
    loadAudioFiles() {
      // 假设已知文件结构，手动生成文件路径
      const models = [
        'ours',
        'ECSS',
        'CONCSSS',
      ];
      const files = ['4_0_d176.wav', '4_1_d263.wav', '9_1_d1496.wav']; // 假设文件名已知

      this.tableDatas = files.map((file) => {
        return {
          text: file,
          tableData: models.map((model) => {
            return {
              model: model,
              audio: `../../static/audio/${model}/${file}`, // 使用相对路径
              scores1: 0,
              scores2: 0,
            };
          }),
        };
      });
    },
    exportToJson() {
      const exportData = {
        score1: [],
        score2: [],
      };
    
      this.tableDatas.forEach((table) => {
        const score1Row = [];
        const score2Row = [];
        table.tableData.forEach((row) => {
          score1Row.push(row.scores1);
          score2Row.push(row.scores2);
        });
        exportData.score1.push(score1Row);
        exportData.score2.push(score2Row);
      });
    
      const jsonData = JSON.stringify(exportData, null, 2);
      const blob = new Blob([jsonData], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
    
      const a = document.createElement('a');
      a.href = url;
      a.download = 'scores.json';
      a.click();
    
      URL.revokeObjectURL(url);
    },

    clearInput(row, key) {
      row[key] = '';
    },
    detectDevice() {
      uni.getSystemInfo({
        success: (res) => {
          if (res.screenWidth <= 768) {
            this.isMobile = true;
            uni.showModal({
              title: 's2lab小提示',
              content: '请使用pc网页访问,点击进入小游戏',
              showCancel: false,
              success: (res) => {
                if (res.confirm) {
                  uni.navigateTo({ url: '/pages/index/game' });
                }
              },
            });
          }
        },
      });
    },
  },
};
</script>

<style scoped>
.container {
  padding: 20px;
}

.header {
  font-size: 24px;
  text-align: center;
  margin-bottom: 20px;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.row {
  display: flex;
  align-items: center;
  border-bottom: 1px solid #ddd;
}

.header-row {
  font-weight: bold;
}

.cell {
  flex: 1;
  padding: 10px;
  text-align: center;
}

.export-btn {
  background-color: #4caf50;
  color: white;
  text-align: center;
  padding: 10px;
  margin-top: 20px;
  cursor: pointer;
}
</style>
