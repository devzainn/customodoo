document.addEventListener('DOMContentLoaded', function () {
    const pengeluaranCanvas = document.getElementById("pengeluaranPieChart");
    const usageCanvas = document.getElementById("produkHistogram");

    if (pengeluaranCanvas) {
        try {
            const pengeluaranData = JSON.parse(pengeluaranCanvas.dataset.produkPengeluaran);
            const labels = Object.keys(pengeluaranData);
            const data = Object.values(pengeluaranData);

            new Chart(pengeluaranCanvas, {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Pengeluaran',
                        data: data,
                        backgroundColor: [
                            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'
                        ],
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        tooltip: {
                            callbacks: {
                                label: (context) => `${context.label}: ${context.raw} (Rp)`
                            }
                        }
                    }
                }
            });
        } catch (error) {
            console.error("Error Parsing Pengeluaran JSON:", error);
        }
    }

    // Histogram untuk Usage Produk
    if (usageCanvas) {
        try {
            const usageData = JSON.parse(usageCanvas.dataset.produkUsage);
            const labels = Object.keys(usageData);
            const data = Object.values(usageData);

            new Chart(usageCanvas, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Usage',
                        data: data,
                        backgroundColor: '#36A2EB',
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Produk'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Jumlah Penggunaan'
                            }
                        }
                    }
                }
            });
        } catch (error) {
            console.error("Error Parsing Usage JSON:", error);
        }
    }
});