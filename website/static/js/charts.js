class Charts {
  constructor() {
    document.addEventListener("DOMContentLoaded", () => {
      this.initializeCharts();
    })

  }

  initializeCharts() {
    const chartHistoryElement = document.getElementById('chart_history');
    const chartContractElement = document.getElementById('chart_contract');

    if (chartHistoryElement) {
      const ctx = chartHistoryElement.getContext('2d');
      new Chart(ctx, {
        type: 'line',

        data: {
          labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
          datasets: [{
            label: "",
            data: [12, 19, 10, 8, 10, 13],
            borderWidth: 1,
            fill: true,
          }]
        },
        options: {
          scales: {
            x: {
              grid: {
                display: false,
              },
              ticks: {
                display: false,
              }
            },
            y: {
              grid: {
                display: false,
              },
              ticks: {
                display: false,
              }
            },
          },

        }
      });

    } else {
      console.warn('Elemento chart_history não encontrado.');
    }

    if (chartContractElement) {
      const cty = chartContractElement.getContext('2d');
      new Chart(cty, {
        type: 'line',

        data: {
          labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
          datasets: [{
            label: "",
            data: [12, 19, 10, 8, 10, 13],
            borderWidth: 1,
            fill: true,
          }]
        },
        options: {
          scales: {
            x: {
              grid: {
                display: false,
              },
              ticks: {
                display: false,
              }
            },
            y: {
              grid: {
                display: false,
              },
              ticks: {
                display: false,
              }
            },
          },

        }
      });
    } else {
      console.warn('Elemento chart_contract não encontrado.');
    }
  }

}

const chart = new Charts();


