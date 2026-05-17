(function () {
  const form = document.getElementById("ticket-intake");
  if (!form) return;

  const status = document.getElementById("ticket-status");
  const moneyDate = () => new Date().toISOString().slice(0, 10);

  function setStatus(message, kind) {
    if (!status) return;
    status.textContent = message;
    status.dataset.kind = kind || "info";
  }

  function checkedValues(name) {
    return Array.from(form.querySelectorAll(`input[name="${name}"]:checked`)).map((el) => el.value);
  }

  function fieldValue(name) {
    const field = form.elements[name];
    return field ? String(field.value || "").trim() : "";
  }

  function escapeHtml(value) {
    return String(value || "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function paragraphize(value) {
    return escapeHtml(value)
      .split(/\n{2,}/)
      .map((part) => part.replace(/\n/g, "<br>"))
      .map((part) => `<p>${part}</p>`)
      .join("");
  }

  function addValue(values, name, value) {
    if (value === undefined || value === null || value === "") return;
    values.push({ name, value: String(value) });
  }

  function addMulti(values, name, items) {
    items.filter(Boolean).forEach((value, index) => {
      const row = { name, value: String(value) };
      if (index) row.place = index;
      values.push(row);
    });
  }

  function buildDescription() {
    const details = fieldValue("description_plain");
    const sourceNotes = fieldValue("source_notes");
    const submitter = [fieldValue("submitter_name"), fieldValue("submitter_email")].filter(Boolean).join(" / ");
    let html = `<p><strong>Submitted through the Airdrie client-facing HTML intake.</strong></p>`;
    if (submitter) html += `<p><strong>Submitter:</strong> ${escapeHtml(submitter)}</p>`;
    html += `<p><strong>Request details</strong></p>${paragraphize(details)}`;
    if (sourceNotes) {
      html += `<p><strong>Source files, links, or context to attach after submission</strong></p>${paragraphize(sourceNotes)}`;
    }
    return html;
  }

  function buildPayload() {
    const values = [];
    const topics = checkedValues("ticket_topic");
    const outputs = checkedValues("output_format");
    const today = moneyDate();
    const submitter = [fieldValue("submitter_name"), fieldValue("submitter_email")].filter(Boolean).join(" / ");

    addValue(values, "ticket_name", fieldValue("ticket_name"));
    addMulti(values, "ticket_topic", topics.length ? topics : ["Other"]);
    addValue(values, "description", buildDescription());
    addValue(values, "objective", fieldValue("objective"));
    addValue(values, "urgency", fieldValue("urgency") || "medium");
    addValue(values, "required_completion_date", fieldValue("required_completion_date"));
    addValue(values, "date_submitted", today);
    addValue(values, "geographic_scope", fieldValue("geographic_scope") || "City of Airdrie");
    addMulti(values, "output_format", outputs.length ? outputs : ["docx"]);
    addValue(values, "content_volume", fieldValue("content_volume"));
    addValue(values, "est_hrs", fieldValue("est_hrs"));
    addValue(values, "brand", form.elements.brand && form.elements.brand.checked ? "1" : "0");
    addValue(values, "private_ticket", fieldValue("private_ticket") || "0");
    addValue(values, "t_ticket_event_status", "Submitted");
    addValue(
      values,
      "status_notes",
      `Submitted via Airdrie client-facing HTML intake on ${today}.${submitter ? ` Submitter: ${submitter}.` : ""} Source attachments remain in protected Karto records.`
    );

    return { values };
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    const endpoint = form.dataset.endpoint;
    const submit = form.querySelector('button[type="submit"]');
    submit.disabled = true;
    setStatus("Submitting to Karto...", "info");

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(buildPayload()),
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok || data.error) {
        const message = data.error && data.error.message ? data.error.message : `HTTP ${response.status}`;
        throw new Error(message);
      }
      const recordID = data.response && data.response.recordID ? data.response.recordID : "";
      setStatus(recordID ? `Submitted. Ticket record ${recordID} created.` : "Submitted. Ticket record created.", "success");
      form.reset();
      const brand = form.elements.brand;
      if (brand) brand.checked = true;
    } catch (error) {
      setStatus(
        `Could not submit from this page: ${error.message}. Confirm you are signed into Karto, then retry. If it still fails, use the protected Karto record layer for attachments and admin entry.`,
        "error"
      );
    } finally {
      submit.disabled = false;
    }
  });
})();
