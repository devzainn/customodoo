$(document).ready(function () {
    function createBarChart(chartElement, chartTitle, data) {
        new Chart(chartElement, {
            type: 'bar',
            data: {
                labels: Object.keys(data),
                datasets: [{
                    label: chartTitle,
                    data: Object.values(data),
                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    xAxes: [{
                        ticks: {
                            autoSkip: false
                        }
                    }],
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    }

    function createLineChart(chartElement, chartTitle, data) {
        new Chart(chartElement, {
            type: 'line',
            data: {
                labels: data.map(item => item.tanggal),
                datasets: [{
                    label: chartTitle,
                    data: data.map(item => item.jumlah),
                    backgroundColor: 'rgba(153, 102, 255, 0.6)',
                    borderColor: 'rgba(153, 102, 255, 1)',
                    fill: false,
                    tension: 0.1
                }]
            },
            options: {
                scales: {
                    xAxes: [{
                        type: 'time',
                        time: {
                            parser: 'YYYY-MM-DD',
                            tooltipFormat: 'll',
                            unit: 'month',
                            displayFormats: {
                                month: 'MMM YYYY'
                            }
                        }
                    }],
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    }

    // Data yang diambil dari backend harus di-inject ke dalam script ini
    if (typeof dashboardData !== 'undefined') {
        if (dashboardData.produk_pengeluaran) {
            createBarChart(document.getElementById('produk_pengeluaran_chart'), 'Pengeluaran per Produk', dashboardData.produk_pengeluaran);
        }
        if (dashboardData.payment_history) {
            createLineChart(document.getElementById('payment_history_chart'), 'Riwayat Pembayaran', dashboardData.payment_history);
        }
    }
});
