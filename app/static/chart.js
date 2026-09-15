const SERIES = [
  { key: "cost", label: "Cost", color: "#fcf792" },
  { key: "cpa", label: "CPA", color: "#3670fc" },
  { key: "roi_confirmed", label: "ROI confirmed", color: "#118603" },
  { key: "conversions", label: "Conversions", color: "#b601fc" },
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

function hiddenValueAxis(max) {
  return {
    type: "value",
    min: 0,
    max,
    axisLabel: { show: false },
    axisTick: { show: false },
    axisLine: { show: false },
    splitLine: { show: false },
  };
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
      borderColor: "#9d9d9d",
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
          color: "rgba(120, 120, 120, 0.16)",
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
    // У метрик разные единицы измерения. Отдельные скрытые шкалы нужны не только для
    // читаемости значений, но и для сохранения визуальных пропорций исходного графика.
    yAxis: [
      hiddenValueAxis(75),
      hiddenValueAxis(750),
      hiddenValueAxis(100),
      hiddenValueAxis(100),
    ],
    series: [
      {
        name: "Cost",
        type: "line",
        yAxisIndex: 0,
        data: data.cost,
        symbol: "none",
        connectNulls: false,
        lineStyle: { color: "#fcf792", width: 1.5 },
        areaStyle: { color: "#fcecbb", opacity: 1 },
        emphasis: { disabled: true },
        z: 1,
      },
      {
        name: "CPA",
        type: "bar",
        yAxisIndex: 3,
        data: data.cpa,
        barWidth: 34,
        itemStyle: {
          color: "#3670fc",
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
        smooth: 0.42,
        showSymbol: false,
        symbol: "diamond",
        symbolSize: 8,
        lineStyle: { color: "#118603", width: 2 },
        itemStyle: {
          color: "#118603",
          borderColor: "#ffffff",
          borderWidth: 1.5,
        },
        connectNulls: false,
        z: 5,
      },
      {
        name: "Conversions",
        type: "line",
        yAxisIndex: 2,
        data: data.conversions,
        smooth: false,
        symbol: "rect",
        symbolSize: 11,
        lineStyle: { color: "#b601fc", width: 2 },
        itemStyle: { color: "#b601fc" },
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
