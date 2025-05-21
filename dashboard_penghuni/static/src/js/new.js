odoo.define("dashboard_penghuni.new", function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var QWeb = core.qweb;

    var ChartVisualization = AbstractAction.extend({
        template: 'ChartVisualization',
        cssLibs: [],
        jsLibs: [],
        events: {},

        init: function (parent, action) {
            this._super(parent, action);
        },

        start: function () {
            this._renderCharts();
        },

        _renderCharts: function () {
            var self = this;
            var chartsData = {
                'statistikUmum': statistik_umum_data,
                'pengeluaran': pengeluaran_data,
                'produkUsage': produk_usage_data
            };

            for (var chartName in chartsData) {
                var chartElement = document.getElementById(chartName + 'Chart');
                if (chartElement) {
                    this._createChart(chartElement, chartName, chartsData[chartName]);
                }
            }
        },

        _createChart: function (chartElement, chartTitle, data) {
            new Chart(chartElement, {
                type: 'bar',
                data: {
                    labels: data['labels'],
                    datasets: data['datasets']
                },
                options: {
                    plugins: {
                        title: {
                            display: true,
                            text: chartTitle.toUpperCase()
                        }
                    },
                    scales: {
                        x: {
                            type: 'category',
                            ticks: {
                                callback: function (label) {
                                    return label.split(";")[0];
                                }
                            }
                        },
                        y: {
                            position: 'left',
                            scaleLabel: {
                                display: true,
                                labelString: 'Value'
                            },
                            ticks: {
                                beginAtZero: true
                            }
                        }
                    }
                }
            });
        }
    });

    core.action_registry.add("new", ChartVisualization);
    return ChartVisualization;
});
