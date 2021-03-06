let transactionCountByYearChart;
let transactionPricesByYearChart;

const earliestDataYear = 1995;
const currentYear = new Date().getFullYear();

google.charts.load('current', {packages: ['corechart', 'table']});

const titleCase = str => {
  try {
    str = str.toLowerCase().split(' ');
    for (const i in str) {
      str[i] = str[i].charAt(0).toUpperCase() + str[i].slice(1);
    }
    return str.join(' ');
  } catch (TypeError) {
    return "";
  }
};


const updateAddress = (address) => {
  let content = `<div>Postcode: ${address.postcode}</div>`;
  content += `<div>${address.admin_district}, ${address.region}, ${address.country} </div>`;
  document.querySelector('#address').innerHTML = content;
};


const updateMap = (latLng) => {
  // note: `map` var is defined outside in google_map.js, which is generated by flask-googlemaps
  // update map to center around current latLng
  map.setCenter(latLng);

  // clear existing markers by setting associated map to null
  for (let i = 0; i < map_markers.length; i++) {
    map_markers[i].setMap(null);
  }
  map_markers = [];

  // add new marker for current latLng
  var marker = new google.maps.Marker({
    position: latLng,
    map: map,
  });
  map_markers.push(marker)
};


const updateTransactionCountByYearChart = chartData => {
  if (transactionCountByYearChart) {
    transactionCountByYearChart.destroy();
  }

  const ctx = document.getElementById('transaction-count-by-year').getContext('2d');
  transactionCountByYearChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: chartData.label,
      datasets: [{
        label: 'No. of Transactions',
        data: chartData.data,
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1
      }]
    },
    options: {
      title: {
        display: true,
        text: 'No. of Transactions by Year'
      },
      legend: {
        display: false,
      },
      scales: {
        yAxes: [{
          scaleLabel: {
            display: true,
            labelString: 'No. of transactions'
          },
          ticks: {
            beginAtZero: true,
            suggestedMax: 10,
            min: 0,
          }
        }],
        xAxes: [{
          ticks: {
            min: earliestDataYear,
            max: currentYear,
            stepSize: 1
          }
        }]
      }
    }
  });
};


const updateTransactionPricesByYearChart = chartData => {
  if (transactionPricesByYearChart) {
    transactionPricesByYearChart.destroy();
  }
  const ctx = document.getElementById('transaction-prices-by-year').getContext('2d');
  transactionPricesByYearChart = new Chart(ctx, {
    type: 'scatter',
    data: {
      labels: 'Transaction Prices',
      datasets: [{
        label: 'Transaction Price',
        data: chartData.data,
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1
      }]
    },
    options: {
      title: {
        display: true,
        text: 'Transaction Prices by Year'
      },
      legend: {
        display: false,
      },
      scales: {
        yAxes: [{
          scaleLabel: {
            display: true,
            labelString: 'Transaction Price (£)'
          },
          ticks: {
            beginAtZero: true,
            min: 0,
          }
        }],
        xAxes: [{
          ticks: {
            min: earliestDataYear,
            max: currentYear,
            stepSize: 1
          }
        }]
      }
    }
  });
};


const updateCharts = charts => {
  updateTransactionCountByYearChart(charts.transactionCountByYear);
  updateTransactionPricesByYearChart(charts.transactionPricesByYear);
};


const updateTransactionTable = transactions => {
  const options = {
    showRowNumber: true,
    allowHtml: true,
    width: '100%',
    height: '100%'
  };

  const data = new google.visualization.DataTable();
  data.addColumn('string', 'Date');
  data.addColumn('string', 'Estate type');
  data.addColumn('string', 'Property type');
  data.addColumn('number', 'Price paid');
  data.addColumn('string', 'PAON');
  data.addColumn('string', 'SAON');
  data.addColumn('string', 'Street');
  data.addColumn('string', 'Town');
  data.addColumn('string', 'County');
  data.addColumn('string', 'Postcode');
  const rows = [];
  transactions.forEach(function (row) {
    rows.push([
      row.transaction_date,
      titleCase(row.estate_type.split('/').pop()),
      titleCase(row.property_type.split('/').pop()),
      parseFloat(row.price_paid),
      titleCase(row.paon),
      titleCase(row.saon),
      titleCase(row.street),
      titleCase(row.town),
      titleCase(row.county),
      row.postcode
    ])
  });

  data.addRows(rows);

  const table = new google.visualization.Table(document.getElementById('transactions'));
  table.draw(data, options);
};


const pollForMapInitialisation = () => {
  if (map !== null) {
    document.querySelector('#submit-button').click();
  } else {
    setTimeout(pollForMapInitialisation, 100);
  }
};


document.addEventListener('DOMContentLoaded', () => {

  document.querySelector('#form').onsubmit = () => {

    const request = new XMLHttpRequest();

    request.open('POST', '/postcode');

    request.onload = () => {
      const data = JSON.parse(request.responseText);

      if (data.success) {
        updateAddress(data.address);
        updateMap({lat: data.address.latitude, lng: data.address.longitude});
        updateCharts(data.charts);
        updateTransactionTable(data.transactions);
        document.querySelector('#error-msg').innerHTML = '';
      }
      else {
        document.querySelector('#error-msg').innerHTML = 'Error: ' + data.errorMessage;
        document.querySelector('#error-msg').style.color = '#CD0618';
      }
    };

    const data = new FormData();
    const postcode = document.querySelector('#postcode-input').value;
    data.append('postcode', postcode);
    request.send(data);

    return false;
  };

  document.querySelector('#postcode-input').onkeyup = () => {
    if (document.getElementById("postcode-input").value === "") {
      document.getElementById('submit-button').disabled = true;
    } else {
      document.getElementById('submit-button').disabled = false;
    }
  };

  // initialise page with default postcode
  document.querySelector('#postcode-input').value = "W1W 5DG";

  setTimeout(pollForMapInitialisation, 100);
});
