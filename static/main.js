
let localData = 'http://127.0.0.1:5000/api/gas/prices';
let onlineData = 'https://pricinhub.herokuapp.com/api/gas/prices';

let currentApiURL = onlineData;

if( window.location.href != 'https://pricinhub.herokuapp.com/' ){
  currentApiURL = localData;
}else{
  currentApiURL = onlineData;
}

fetch(currentApiURL)
  .then(res => res.json())
  .then(spec => renderTable(spec))
  .catch(err => console.error(err));

function renderTable(data) {

  // Take away the loading indication
  var element = document.getElementById("loader_loding");
  element.parentNode.removeChild(element);

  let newChartData = [];
  let newChartDataLabels = [];

  // Go over each data and append to the table and chart
  dataResponse = data.response;
  dataResponse.map((data, index) => {

    var z = document.createElement('tr'); // is a node
    z.innerHTML = `<td> ${data[0]} </td> <td> ${data[1]} </td>`
    document.getElementById("pricing_data_table").appendChild(z);

    newChartData.push(Number(data[1])); // Push the numbers of the data
    newChartDataLabels.push(data[0]); // Push the labels of the chart

  })


  var ctx = document.getElementById('myChart').getContext('2d');

  var gradientStroke = ctx.createLinearGradient(500, 0, 100, 0);
  // gradientStroke.addColorStop(0, "#80b6f4");
  // gradientStroke.addColorStop(1, "#f49080");

  gradientStroke.addColorStop(0, "#80b6f4");
  gradientStroke.addColorStop(0.2, "#94d973");
  gradientStroke.addColorStop(0.5, "#fad874");
  gradientStroke.addColorStop(1, "#f49080");

  var gradientFill = ctx.createLinearGradient(500, 0, 100, 0);
  gradientFill.addColorStop(0, "rgba(128, 182, 244, 0.6)");
  gradientFill.addColorStop(1, "rgba(244, 144, 128, 0.6)");

  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: newChartDataLabels,
      datasets: [{
        label: 'Pricing Data by date',
        data: newChartData,

        borderColor:               gradientStroke,
        pointBorderColor:          gradientStroke,
        pointBackgroundColor:      gradientStroke,
        pointHoverBackgroundColor: gradientStroke,
        pointHoverBorderColor:     gradientStroke,

        pointBorderWidth: 1,
        pointHoverRadius: 1,
        pointHoverBorderWidth: 1,
        pointRadius: 1,
        fill: true,
        backgroundColor: gradientFill,
        borderWidth: 1,
      }]
    },
    options: {
      legend: {
        position: "bottom"
      },
      scales: {
        yAxes: [{
          ticks: {
            fontColor: "rgb(255, 255, 255)",
            fontStyle: "normal",
            beginAtZero: true,
            maxTicksLimit: 5,
            padding: 1
          },
          gridLines: {
            drawTicks: false,
            display: false
          }
        }],
        xAxes: [{
          gridLines: {
            zeroLineColor: "transparent"
          },
          ticks: {
            padding: 1,
            fontColor: "rgb(255, 255, 255)",
            fontStyle: "normal"
          }
        }]
      },
      animation: {
        easing: "easeInOutBack"
      }
    }
  });

}


function openCSVDownload(){
  window.open(`${window.location.href}static/henry_hub_natural_gas_daily_prices.csv`, '_blank');
}