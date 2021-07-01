var script_tag = document.getElementById('import');
var admindata = script_tag.getAttribute("data");

console.log(admindata);

var ctx = document.getElementById('salesByBrandBar').getContext('2d');
var orderChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Nike', 'Adidas', 'Vans', 'Converse'],
        datasets: [{
            label: 'Total sales',
            data: [12, 19, 3, 5, 2, 3],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});