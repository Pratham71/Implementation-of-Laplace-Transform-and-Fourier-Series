async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }
  return response.json();
}

function setText(id, value) {
  const element = document.getElementById(id);
  if (element) {
    element.textContent = value;
  }
}

function renderList(id, title, items) {
  const host = document.getElementById(id);
  if (!host) {
    return;
  }

  host.innerHTML = "";

  const heading = document.createElement("p");
  heading.innerHTML = `<strong>${title}:</strong>`;
  host.appendChild(heading);

  const list = document.createElement("ul");
  for (const item of items) {
    const entry = document.createElement("li");
    entry.textContent = item;
    list.appendChild(entry);
  }
  host.appendChild(list);
}

function renderVariablesTable(id, variables) {
  const host = document.getElementById(id);
  if (!host) {
    return;
  }

  const rows = variables
    .map(
      (variable) =>
        `<tr><td><strong>${variable.symbol}</strong></td><td>${variable.meaning}</td></tr>`,
    )
    .join("");

  host.innerHTML = `
    <div class="table-wrap">
      <table>
        <caption class="muted">Model variables</caption>
        <thead>
          <tr><th scope="col">Symbol</th><th scope="col">Meaning</th></tr>
        </thead>
        <tbody>${rows}</tbody>
      </table>
    </div>
  `;
}

function renderFourierCoefficients(coefficients) {
  const host = document.getElementById("fourier-coefficients");
  if (!host || !coefficients) {
    return;
  }

  const rows = coefficients.terms
    .map(
      (coefficient) =>
        `<tr><td>${coefficient.n}</td><td>${formatMetric(coefficient.an)}</td><td>${formatMetric(coefficient.bn)}</td><td><code>${coefficient.term}</code></td></tr>`,
    )
    .join("");

  host.innerHTML = `
    <p><strong>a0:</strong> ${formatMetric(coefficients.a0)}</p>
    <p><strong>an:</strong> ${coefficients.an_note}</p>
    <p><strong>bn formula:</strong> <code>${coefficients.bn_formula}</code></p>
    <div class="table-wrap">
      <table>
        <caption class="muted">Showing the first ${coefficients.terms.length} coefficient terms</caption>
        <thead>
          <tr>
            <th scope="col">n</th>
            <th scope="col">an</th>
            <th scope="col">bn</th>
            <th scope="col">Term</th>
          </tr>
        </thead>
        <tbody>${rows}</tbody>
      </table>
    </div>
  `;
}

function renderCoefficientChart(coefficients) {
  const terms = coefficients?.terms ?? [];
  if (!terms.length) {
    setDownloadEnabled("download-fourier-coefficients", false);
    return;
  }

  const nValues = terms.map((coefficient) => coefficient.n);
  const anValues = terms.map((coefficient) => coefficient.an);
  const bnValues = terms.map((coefficient) => coefficient.bn);

  renderChart(
    "fourier-coefficient-chart",
    [
      {
        label: "Cosine coefficient a_n",
        x: nValues,
        y: anValues,
        color: "#7a8790",
        width: 2.25,
      },
      {
        label: "Sine coefficient b_n",
        x: nValues,
        y: bnValues,
        color: "#b74d27",
        width: 3,
      },
    ],
    "Coefficient index n",
    "Coefficient value",
    "x-axis = term index n; y-axis = Fourier coefficients a_n and b_n",
  );
  setDownloadEnabled("download-fourier-coefficients", true);
}

function formatNumber(value) {
  return Number.parseFloat(value).toFixed(2);
}

function formatMetric(value) {
  const numericValue = Number.parseFloat(value);
  if (!Number.isFinite(numericValue)) {
    return String(value);
  }
  if (Math.abs(numericValue) < 0.001 && numericValue !== 0) {
    return numericValue.toExponential(2);
  }
  return numericValue.toFixed(4);
}

function renderMetrics(id, metrics) {
  const host = document.getElementById(id);
  if (!host) {
    return;
  }

  host.innerHTML = "";
  for (const metric of metrics) {
    const wrapper = document.createElement("div");
    const term = document.createElement("dt");
    const description = document.createElement("dd");

    term.textContent = metric.label;
    description.textContent = metric.value;
    wrapper.append(term, description);
    host.appendChild(wrapper);
  }
}

function createPolyline(points, color, width) {
  return `<polyline fill="none" stroke="${color}" stroke-width="${width}" stroke-linecap="round" stroke-linejoin="round" points="${points}" />`;
}

function escapeSvgText(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function createLegend(series) {
  const itemWidth = 210;
  return series
    .map((entry, index) => {
      const x = 48 + index * itemWidth;
      const label = escapeSvgText(entry.label ?? `Series ${index + 1}`);

      return `
        <g transform="translate(${x} 15)">
          <line x1="0" y1="0" x2="28" y2="0" stroke="${entry.color}" stroke-width="${entry.width}" stroke-linecap="round" />
          <text x="36" y="4" fill="#3f484c" font-size="12" font-weight="700">${label}</text>
        </g>
      `;
    })
    .join("");
}

function setDownloadEnabled(buttonId, enabled) {
  const button = document.getElementById(buttonId);
  if (!button) {
    return;
  }
  button.disabled = !enabled;
}

function renderChart(svgId, series, xLabel, yLabel, guideText) {
  const svg = document.getElementById(svgId);
  if (!svg || !series.length) {
    return;
  }

  const width = 640;
  const height = 260;
  const padding = { top: 44, right: 20, bottom: 34, left: 48 };
  const xs = series.flatMap((entry) => entry.x);
  const ys = series.flatMap((entry) => entry.y);
  const minX = Math.min(...xs);
  const maxX = Math.max(...xs);
  const minY = Math.min(...ys);
  const maxY = Math.max(...ys);
  const xRange = maxX - minX || 1;
  const yRange = maxY - minY || 1;

  const toPointString = (xValues, yValues) =>
    xValues
      .map((x, index) => {
        const y = yValues[index];
        const mappedX =
          padding.left + ((x - minX) / xRange) * (width - padding.left - padding.right);
        const mappedY =
          height -
          padding.bottom -
          ((y - minY) / yRange) * (height - padding.top - padding.bottom);
        return `${mappedX.toFixed(2)},${mappedY.toFixed(2)}`;
      })
      .join(" ");

  const gridLines = Array.from({ length: 5 }, (_, index) => {
    const y = padding.top + (index / 4) * (height - padding.top - padding.bottom);
    return `<line x1="${padding.left}" y1="${y}" x2="${width - padding.right}" y2="${y}" stroke="rgba(31, 35, 38, 0.08)" stroke-width="1" />`;
  }).join("");

  const lines = series
    .map((entry) => createPolyline(toPointString(entry.x, entry.y), entry.color, entry.width))
    .join("");
  const legend = createLegend(series);
  const safeXLabel = escapeSvgText(xLabel);
  const safeYLabel = escapeSvgText(yLabel);
  const safeGuideText = escapeSvgText(guideText);

  svg.innerHTML = `
    <rect x="0" y="0" width="${width}" height="${height}" rx="18" fill="transparent"></rect>
    ${legend}
    ${gridLines}
    <line x1="${padding.left}" y1="${height - padding.bottom}" x2="${width - padding.right}" y2="${height - padding.bottom}" stroke="rgba(31, 35, 38, 0.18)" stroke-width="1.5" />
    <line x1="${padding.left}" y1="${padding.top}" x2="${padding.left}" y2="${height - padding.bottom}" stroke="rgba(31, 35, 38, 0.18)" stroke-width="1.5" />
    ${lines}
    <text x="${width / 2}" y="${height - 20}" text-anchor="middle" fill="#5b6468" font-size="12">${safeXLabel}</text>
    <text x="16" y="${height / 2}" text-anchor="middle" fill="#5b6468" font-size="12" transform="rotate(-90 16 ${height / 2})">${safeYLabel}</text>
    <text x="${padding.left}" y="${padding.top - 4}" fill="#5b6468" font-size="11">${formatNumber(maxY)}</text>
    <text x="${padding.left}" y="${height - padding.bottom + 14}" fill="#5b6468" font-size="11">${formatNumber(minY)}</text>
    <text x="${width / 2}" y="${height - 7}" text-anchor="middle" fill="#5b6468" font-size="10">${safeGuideText}</text>
  `;
}

async function downloadChartAsPng(chartId, filename) {
  const svg = document.getElementById(chartId);
  if (!svg || !svg.innerHTML.trim()) {
    throw new Error("Chart is not ready");
  }

  const serialized = new XMLSerializer().serializeToString(svg);
  const blob = new Blob([serialized], { type: "image/svg+xml;charset=utf-8" });
  const objectUrl = URL.createObjectURL(blob);

  try {
    const image = new Image();
    image.decoding = "async";

    await new Promise((resolve, reject) => {
      image.onload = resolve;
      image.onerror = reject;
      image.src = objectUrl;
    });

    const viewBox = svg.viewBox.baseVal;
    const width = viewBox.width || svg.clientWidth || 640;
    const height = viewBox.height || svg.clientHeight || 260;
    const canvas = document.createElement("canvas");
    const scale = 2;
    canvas.width = width * scale;
    canvas.height = height * scale;

    const context = canvas.getContext("2d");
    if (!context) {
      throw new Error("Canvas context unavailable");
    }

    context.fillStyle = "#fffaf4";
    context.fillRect(0, 0, canvas.width, canvas.height);
    context.scale(scale, scale);
    context.drawImage(image, 0, 0, width, height);

    const dataUrl = canvas.toDataURL("image/png");
    const link = document.createElement("a");
    link.href = dataUrl;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
  } finally {
    URL.revokeObjectURL(objectUrl);
  }
}

async function loadLaplaceContent() {
  const data = await fetchJson("/api/applications/laplace");

  setText("laplace-description", data.description);
  setText("laplace-learning-objective", data.learning_objective);
  setText("laplace-equation", data.equation);
  setText("laplace-why", data.why_laplace);
  setText("laplace-interpretation", data.interpretation);
  setText("laplace-assignment", data.assignment_link);
  renderVariablesTable("laplace-variables", data.variables);
  renderList("laplace-use-cases", "Use cases", data.use_cases);
  renderList("laplace-limitations", "Limitations", data.limitations);
}

async function loadFourierContent() {
  const data = await fetchJson("/api/applications/fourier");

  setText("fourier-description", data.description);
  setText("fourier-learning-objective", data.learning_objective);
  setText("fourier-equation", data.series_equation);
  setText("fourier-concept", data.concept);
  setText("fourier-interpretation", data.interpretation);
  setText("fourier-assignment", data.assignment_link);
  renderList("fourier-steps", "Compression steps", data.steps);
  renderList("fourier-use-cases", "Use cases", data.use_cases);
  renderList("fourier-limitations", "Limitations", data.limitations);
}

async function loadLaplaceSimulation() {
  const form = document.getElementById("laplace-form");
  const status = document.getElementById("laplace-status");
  const params = new URLSearchParams(new FormData(form));
  status.textContent = "Running simulation...";

  try {
    const data = await fetchJson(`/api/applications/laplace/simulate?${params.toString()}`);
    status.textContent =
      "Simulation ready. Compare displacement against the applied forcing signal.";

    renderChart(
      "laplace-chart",
      [
        { label: "Displacement y(t)", x: data.t, y: data.displacement, color: "#0d6b78", width: 3 },
        { label: "Applied force F(t)", x: data.t, y: data.forcing, color: "#4f8d6f", width: 2.25 },
      ],
      "Time (s)",
      "Response",
      "x-axis = sampled time index t; y-axis = displacement/forcing response",
    );
    renderMetrics("laplace-error-analysis", [
      {
        label: "Solver status",
        value: data.error_analysis.solver_success ? "Success" : "Check solver",
      },
      {
        label: "Max residual",
        value: formatMetric(data.error_analysis.max_ode_residual),
      },
      {
        label: "Mean residual",
        value: formatMetric(data.error_analysis.mean_ode_residual),
      },
      {
        label: "Tolerance",
        value: `rtol ${data.error_analysis.relative_tolerance}, atol ${data.error_analysis.absolute_tolerance}`,
      },
    ]);
    setDownloadEnabled("download-laplace", true);
  } catch (error) {
    status.textContent =
      "Simulation could not be loaded. Check the parameter values and try again.";
    renderMetrics("laplace-error-analysis", [
      { label: "Solver status", value: "Unavailable" },
    ]);
    setDownloadEnabled("download-laplace", false);
  }
}

async function loadFourierSignal() {
  const form = document.getElementById("fourier-form");
  const status = document.getElementById("fourier-status");
  const params = new URLSearchParams(new FormData(form));
  status.textContent = "Building approximation...";

  try {
    const data = await fetchJson(`/api/applications/fourier/signal?${params.toString()}`);
    status.textContent = `Approximation updated with ${data.terms_used} Fourier terms.`;

    renderChart(
      "fourier-chart",
      [
        { label: "Original signal f(x)=x", x: data.x, y: data.signal, color: "#0d6b78", width: 3 },
        { label: "Fourier approximation", x: data.x, y: data.approximation, color: "#b74d27", width: 2.25 },
      ],
      "x (radians)",
      "Amplitude",
      "x-axis = sampled x index in radians; y-axis = signal amplitude",
    );
    renderMetrics("fourier-error-analysis", [
      {
        label: "Mean absolute error",
        value: formatMetric(data.error_analysis.mean_absolute_error),
      },
      {
        label: "RMS error",
        value: formatMetric(data.error_analysis.root_mean_square_error),
      },
      {
        label: "Max absolute error",
        value: formatMetric(data.error_analysis.max_absolute_error),
      },
      {
        label: "Terms used",
        value: String(data.terms_used),
      },
    ]);
    renderFourierCoefficients(data.coefficients);
    renderCoefficientChart(data.coefficients);
    setDownloadEnabled("download-fourier", true);
  } catch (error) {
    status.textContent =
      "Approximation could not be loaded. Enter a positive number of terms and try again.";
    renderMetrics("fourier-error-analysis", [
      { label: "Approximation status", value: "Unavailable" },
    ]);
    setDownloadEnabled("download-fourier", false);
    setDownloadEnabled("download-fourier-coefficients", false);
  }
}

function bindForms() {
  document.getElementById("laplace-form")?.addEventListener("submit", (event) => {
    event.preventDefault();
    loadLaplaceSimulation();
  });

  document.getElementById("fourier-form")?.addEventListener("submit", (event) => {
    event.preventDefault();
    loadFourierSignal();
  });

  document.querySelectorAll(".chart-download").forEach((button) => {
    button.addEventListener("click", async () => {
      const chartId = button.dataset.chartId;
      const filename = button.dataset.filename;

      if (!chartId || !filename) {
        return;
      }

      const previousText = button.textContent;
      button.disabled = true;
      button.textContent = "Preparing Download...";

      try {
        await downloadChartAsPng(chartId, filename);
      } catch (error) {
        const statusId = chartId === "laplace-chart" ? "laplace-status" : "fourier-status";
        setText(statusId, "Download failed. Re-render the graph and try again.");
      } finally {
        button.textContent = previousText;
        const svg = document.getElementById(chartId);
        button.disabled = !svg || !svg.innerHTML.trim();
      }
    });
  });
}

async function initializePage() {
  bindForms();

  try {
    await Promise.all([loadLaplaceContent(), loadFourierContent()]);
  } catch (error) {
    const message = "Some explanatory content could not be loaded from the API.";
    setText("laplace-description", message);
    setText("fourier-description", message);
  }

  await Promise.allSettled([loadLaplaceSimulation(), loadFourierSignal()]);
}

initializePage();
