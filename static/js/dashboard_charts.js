document.addEventListener("DOMContentLoaded", () => {
  // Chart.js 전역 스타일 설정
  Chart.defaults.color = "#aaaaaa";
  Chart.defaults.borderColor = "#444444";
  Chart.defaults.font.family = "'Noto Sans KR', sans-serif";

  // 일일 조회수 차트 (Line Chart)
  const dailyViewsCtx = document.getElementById("dailyViewsChart");
  if (dailyViewsCtx) {
    new Chart(dailyViewsCtx, {
      type: "line",
      data: {
        labels: Array.from({ length: 28 }, (_, i) => {
          const d = new Date();
          d.setDate(d.getDate() - (27 - i));
          return `${d.getMonth() + 1}/${d.getDate()}`;
        }),
        datasets: [
          {
            label: "조회수",
            data: Array.from(
              { length: 28 },
              () => Math.floor(Math.random() * 5000) + 1000
            ),
            borderColor: "#ff0000",
            backgroundColor: "rgba(255, 0, 0, 0.1)",
            fill: true,
            tension: 0.4,
            pointBackgroundColor: "#ff0000",
            pointRadius: 0,
            pointHoverRadius: 6,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          },
        },
        scales: {
          x: {
            grid: {
              display: false,
            },
          },
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  }

  // 트래픽 소스 차트 (Doughnut Chart)
  const trafficSourceCtx = document.getElementById("trafficSourceChart");
  if (trafficSourceCtx) {
    new Chart(trafficSourceCtx, {
      type: "doughnut",
      data: {
        labels: [
          "YouTube 검색",
          "탐색 기능",
          "외부",
          "직접/알 수 없음",
          "재생목록",
        ],
        datasets: [
          {
            label: "트래픽 소스",
            data: [38, 25, 15, 12, 10],
            backgroundColor: [
              "#ff4d4d",
              "#ff8080",
              "#ffb3b3",
              "#e60000",
              "#b30000",
            ],
            hoverOffset: 4,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "bottom",
          },
        },
      },
    });
  }

  // 시청자 성별 분포 차트 (Doughnut Chart) - 추가
  const genderDistributionCtx = document.getElementById(
    "genderDistributionChart"
  );
  if (genderDistributionCtx) {
    new Chart(genderDistributionCtx, {
      type: "doughnut",
      data: {
        labels: ["남성", "여성", "미지정"],
        datasets: [
          {
            label: "성별 분포",
            data: [65, 32, 3],
            backgroundColor: ["#36a2eb", "#ff6384", "#cccccc"],
            hoverOffset: 4,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "bottom",
          },
        },
      },
    });
  }

  // 상위 시청 국가 차트 (Bar Chart) - 추가
  const topCountriesCtx = document.getElementById("topCountriesChart");
  if (topCountriesCtx) {
    new Chart(topCountriesCtx, {
      type: "bar",
      data: {
        labels: ["대한민국", "미국", "일본", "베트남", "인도네시아"],
        datasets: [
          {
            label: "시청 시간(%)",
            data: [45, 18, 12, 8, 5],
            backgroundColor: [
              "#ff6384",
              "#36a2eb",
              "#ffce56",
              "#4bc0c0",
              "#9966ff",
            ],
          },
        ],
      },
      options: {
        indexAxis: "y", // 수평 막대 차트로 변경
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          },
        },
        scales: {
          x: {
            beginAtZero: true,
            grid: {
              display: false,
            },
          },
          y: {
            grid: { display: false },
          },
        },
      },
    });
  }
});
