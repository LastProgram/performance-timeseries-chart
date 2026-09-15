const SERIES = [
  { key: "cost", label: "Cost", color: "#ffec73" },
  { key: "cpa", label: "CPA", color: "#3974f6" },
  { key: "roi_confirmed", label: "ROI confirmed", color: "#16851f" },
  { key: "conversions", label: "Conversions", color: "#ae00e6" },
];

const chartElement = document.querySelector("#performance-chart");
const errorElement = document.querySelector("#chart-error");

function formatDate(timestamp) {
  const date = new Date(timestamp);
  const day = String(date.getUTCDate()).padStart(2, "0");
  const month = String(date.getUTCMonth() + 1).padStart(2, "0");
  return `${day}.${month}.${date.getUTCFullYear()}`;
}

function formatValue(value) {
  if (value === null || value === undefined) {
    return "—";
  }

  return Number.isInteger(value) ? String(value) : value.toFixed(2);
}

function tooltipHtml(data, dataIndex) {
  const rows = SERIES.map(({ key, label, color }) => {
    const value = data[key][dataIndex];
    return `
      <div class="tooltip-row">
        <span class="tooltip-dot" style="background:${color}"></span>
        <span>${label}: <strong>${formatValue(value)}</strong></span>
      </div>
    `;
  }).join("");

  return `
    <div class="chart-tooltip">
      <div class="tooltip-date">${formatDate(data.timestamps[dataIndex])}</div>
      ${rows}
    </div>
  `;
}

function buildOption(data) {
  return {
    animation: false,
    grid: {
      left: 58,
      right: 54,
      top: 42,
      bottom: 0,
      containLabel: false,
    },
    tooltip: {
      trigger: "axis",
      confine: true,
      backgroundColor: "#ffffff",
      borderColor: "#9f9f9f",
      borderWidth: 1,
      padding: [14, 17],
      textStyle: {
        color: "#222222",
        fontFamily: "Arial, Helvetica, sans-serif",
        fontSize: 17,
      },
      extraCssText:
        "border-radius:7px;box-shadow:0 6px 13px rgba(0,0,0,.32);line-height:1.08;",
      axisPointer: {
        type: "line",
        lineStyle: {
          color: "rgba(120, 120, 120, 0.18)",
          width: 1,
        },
      },
      formatter(params) {
        const firstPoint = Array.isArray(params) ? params[0] : params;
        return tooltipHtml(data, firstPoint.dataIndex);
      },
    },
    xAxis: {
      type: "category",
      boundaryGap: false,
      data: data.timestamps,
      axisLabel: { show: false },
      axisTick: { show: false },
      axisLine: {
        show: true,
        lineStyle: { color: "#aeb8bc", width: 1 },
      },
    },
    yAxis: [
      {
        type: "value",
        min: 0,
        axisLabel: { show: false },
        axisTick: { show: false },
        axisLine: { show: false },
        splitLine: { show: false },
      },
      {
        type: "value",
        min: 0,
        axisLabel: { show: false },
        axisTick: { show: false },
        axisLine: { show: false },
        splitLine: { show: false },
      },
    ],
    series: [
      {
        name: "Cost",
        type: "line",
        data: data.cost,
        symbol: "none",
        connectNulls: false,
        lineStyle: { color: "rgba(255, 226, 79, 0.58)", width: 1 },
        areaStyle: { color: "rgba(255, 232, 126, 0.58)" },
        emphasis: { disabled: true },
        z: 1,
      },
      {
        name: "CPA",
        type: "bar",
        data: data.cpa,
        barWidth: 18,
        itemStyle: {
          color: "#3974f6",
          borderRadius: [3, 3, 0, 0],
        },
        emphasis: { disabled: true },
        z: 4,
      },
      {
        name: "ROI confirmed",
        type: "line",
        yAxisIndex: 1,
        data: data.roi_confirmed,
        smooth: 0.34,
        showSymbol: false,
        symbol: "diamond",
        symbolSize: 8,
        lineStyle: { color: "#16851f", width: 2 },
        itemStyle: { color: "#16851f" },
        connectNulls: false,
        z: 5,
      },
      {
        name: "Conversions",
        type: "line",
        data: data.conversions,
        smooth: false,
        symbol: "rect",
        symbolSize: 10,
        lineStyle: { color: "#ae00e6", width: 2 },
        itemStyle: { color: "#ae00e6" },
        connectNulls: false,
        z: 6,
      },
    ],
  };
}

async function loadChart() {
  try {
    const response = await fetch("/api/chart");
    if (!response.ok) {
      throw new Error(`Chart data request failed with status ${response.status}`);
    }

    const data = await response.json();
    const chart = echarts.init(chartElement, null, { renderer: "canvas" });
    chart.setOption(buildOption(data));

    // Размер задаёт контейнер, поэтому chart нужно синхронизировать и при layout-изменениях без resize окна.
    const observer = new ResizeObserver(() => chart.resize());
    observer.observe(chartElement);
  } catch (error) {
    errorElement.hidden = false;
    errorElement.textContent = error instanceof Error ? error.message : "Unable to render chart";
  }
}

loadChart();
