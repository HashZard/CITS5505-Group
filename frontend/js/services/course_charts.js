
/**
 * Render the rating distribution chart with dynamic data.
 * @param {CanvasRenderingContext2D} ctx - Canvas 2D context
 * @param {Object} ratingData - e.g., {5: 45, 4: 30, 3: 15, 2: 7, 1: 3}
 */
export function renderRatingChart(ctx, ratingData = {}) {
    const orderedRatings = [5, 4, 3, 2, 1].map(star => ratingData[star] || 0);

    new Chart(ctx, {
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
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 50,
                    ticks: {
                        callback: value => value + '%'
                    }
                }
            }
        }
    });
}


export function renderCourseCharts() {
    function getQueryParam(name) {
        const url = new URL(window.location.href);
        return url.searchParams.get(name) || '';
    }

    // popularity trend chart
    const popularityCtx = document.getElementById('popularityChart')?.getContext('2d');
    if (popularityCtx) {
        new Chart(popularityCtx, {
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
                    legend: { display: false },
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
                        title: { display: true, text: 'Number of Reviews' },
                        ticks: { stepSize: 10 }
                    },
                    x: {
                        grid: { display: false },
                        title: { display: true, text: 'Month' }
                    }
                },
                interaction: { intersect: false, mode: 'index' }
            }
        });
    }

    // difficulty donut chart
    const donutCtx = document.getElementById('difficultyDonutChart')?.getContext('2d');
    if (donutCtx) {
        new Chart(donutCtx, {
            type: 'doughnut',
            data: {
                labels: ['Easy (1-3)', 'Medium (4-7)', 'Hard (8-10)'],
                datasets: [{
                    data: [15, 60, 25],
                    backgroundColor: ['rgb(34, 197, 94)', 'rgb(234, 179, 8)', 'rgb(239, 68, 68)'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                cutout: '70%'
            }
        });
    }

    // difficulty bar chart
    const barCtx = document.getElementById('difficultyBarChart')?.getContext('2d');
    if (barCtx) {
        new Chart(barCtx, {
            type: 'bar',
            data: {
                labels: ['Easy (1-3)', 'Medium (4-7)', 'Hard (8-10)'],
                datasets: [{
                    data: [15, 60, 25],
                    backgroundColor: ['rgb(34, 197, 94)', 'rgb(234, 179, 8)', 'rgb(239, 68, 68)'],
                    borderRadius: 5
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: context => context.raw + '%'
                        }
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: value => value + '%'
                        }
                    },
                    y: {
                        grid: { display: false }
                    }
                },
                barPercentage: 0.6,
                categoryPercentage: 0.8
            }
        });
    }

    // rating chart


    // assessment chart
    const assessmentCtx = document.getElementById('assessmentChart')?.getContext('2d');
    if (assessmentCtx) {
        new Chart(assessmentCtx, {
            type: 'pie',
            data: {
                labels: ['Project Work', 'Mid-semester Exam', 'Final Exam'],
                datasets: [{
                    data: [40, 20, 40],
                    backgroundColor: ['rgb(59, 130, 246)', 'rgb(234, 179, 8)', 'rgb(239, 68, 68)'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true,
                            pointStyle: 'circle'
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: context => `${context.label}: ${context.raw}%`
                        }
                    }
                }
            }
        });
    }
}
