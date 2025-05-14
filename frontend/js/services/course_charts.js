let ratingChartInstance = null;
let popularityChartInstance = null;
let assessmentChartInstance = null;

/**
 * Render the rating distribution chart with dynamic data.
 * @param {CanvasRenderingContext2D} ctx - Canvas 2D context
 * @param {Object} ratingData - e.g., {5: 45, 4: 30, 3: 15, 2: 7, 1: 3}
 */
export function renderRatingChart(ctx, ratingData = {}) {
    const orderedRatings = [5, 4, 3, 2, 1].map(star => ratingData[star] || 0);

    // ✅if the chart instance already exists, destroy it before creating a new one
    if (ratingChartInstance) {
        ratingChartInstance.destroy();
    }

    ratingChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['5 ★', '4 ★', '3 ★', '2 ★', '1 ★'],
            datasets: [{
                data: orderedRatings,
                backgroundColor: 'rgb(234, 179, 8)',
                borderRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {display: false},
                tooltip: {
                    callbacks: {
                        label: context => `Votes: ${context.raw}`
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    // ✅ 自动根据最大值生成 y 轴刻度
                    ticks: {
                        precision: 0  // 显示整数
                    },
                    title: {
                        display: true,
                        text: 'Number of Ratings'
                    }
                }
            }
        }
    });
}


export function renderCourseCharts(structure = {}) {
    function getQueryParam(name) {
        const url = new URL(window.location.href);
        return url.searchParams.get(name) || '';
    }

    // popularity trend chart
    const popularityCtx = document.getElementById('popularityChart')?.getContext('2d');
    if (popularityCtx) {
        // ✅ if the chart instance already exists, destroy it before creating a new one
        if (popularityChartInstance) {
            popularityChartInstance.destroy();
        }

        popularityChartInstance = new Chart(popularityCtx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                datasets: [{
                    label: 'Monthly Reviews',
                    data: [15, 25, 30, 35, 45, 40, 50, 45, 40, 35, 30, 25],
                    borderColor: 'rgb(59, 130, 246)',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: 'rgb(59, 130, 246)',
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {display: false},
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        callbacks: {
                            label: context => 'Reviews: ' + context.raw
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {display: true, text: 'Number of Reviews'},
                        ticks: {stepSize: 10}
                    },
                    x: {
                        grid: {display: false},
                        title: {display: true, text: 'Month'}
                    }
                },
                interaction: {intersect: false, mode: 'index'}
            }
        });
    }

    // assessment chart
    const assessmentCtx = document.getElementById('assessmentChart')?.getContext('2d');
    if (!assessmentCtx || !structure) return;

    // 显示顺序和配色方案保持一致
    const order = [
        {key: "finalExam", label: "Final Exam", color: "rgb(239, 68, 68)"},
        {key: "midSemesterExam", label: "Mid-semester Exam", color: "rgb(234, 179, 8)"},
        {key: "projectWork", label: "Project Work", color: "rgb(59, 130, 246)"},
        {key: "assignment", label: "Assignment", color: "rgb(16, 185, 129)"},
        {key: "attendance", label: "Attendance", color: "rgb(139, 92, 246)"}
    ];

    const labels = [];
    const data = [];
    const colors = [];

    order.forEach(item => {
        const part = structure[item.key];
        if (part && part.enabled) {
            labels.push(item.label);
            data.push(part.weight);
            colors.push(item.color);
        }
    });

    // ✅ 如果已经存在图表实例，销毁旧图表
    if (assessmentChartInstance) {
        assessmentChartInstance.destroy();
    }

    assessmentChartInstance = new Chart(assessmentCtx, {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                data,
                backgroundColor: colors,
                borderRadius: 5
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: context => `${context.raw}%`
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: value => value + '%',
                        font: {size: 12}
                    },
                    title: {
                        display: true,
                        text: 'Percentage',
                        font: {size: 14, weight: 'bold'},
                        padding: {top: 10, bottom: 10}
                    }
                },
                y: {
                    grid: {display: false},
                    ticks: {font: {size: 14, weight: 'bold'}}
                }
            },
            barPercentage: 0.8,
            categoryPercentage: 0.9,
            layout: {
                padding: {left: 10, right: 30, top: 20, bottom: 10}
            }
        }
    });
}
