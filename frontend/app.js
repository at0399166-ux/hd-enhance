let type = "image";

const file = document.getElementById("file");

document.querySelectorAll(".tab").forEach((b) => {
  b.onclick = () => {
    document.querySelectorAll(".tab").forEach((x) =>
      x.classList.remove("active")
    );

    b.classList.add("active");
    type = b.dataset.type;

    file.value = "";
    file.accept = type === "image" ? "image/*" : "video/*";

    document.getElementById("fileInfo").classList.add("hidden");
    document.getElementById("download").classList.add("hidden");
    document.getElementById("enhance").disabled = true;
    document.getElementById("status").textContent = "";
  };
});

file.onchange = () => {
  const f = file.files[0];
  if (!f) return;

  const info = document.getElementById("fileInfo");

  info.textContent =
    `${f.name} • ${(f.size / 1024 / 1024).toFixed(1)} MB`;

  info.classList.remove("hidden");
  document.getElementById("enhance").disabled = false;
};

document.getElementById("enhance").onclick = async () => {
  const f = file.files[0];
  if (!f) return;

  const status = document.getElementById("status");
  const btn = document.getElementById("enhance");
  const download = document.getElementById("download");

  btn.disabled = true;
  status.textContent = "Processing… please wait";
  download.classList.add("hidden");

  const fd = new FormData();

  fd.append("file", f);
  fd.append(
    "scale",
    document.getElementById("scale").value
  );
  fd.append(
    "sharpen",
    document.getElementById("sharpen").value
  );
  fd.append(
    "denoise",
    document.getElementById("denoise").checked ? "1" : "0"
  );

  try {
    const url =
      type === "image"
        ? "/api/enhance/image"
        : "/api/enhance/video";

    const response = await fetch(url, {
      method: "POST",
      body: fd
    });

    // Read response safely
    const text = await response.text();

    let data = {};

    if (text) {
      try {
        data = JSON.parse(text);
      } catch {
        throw new Error(
          `Server returned an invalid response (${response.status})`
        );
      }
    }

    if (!response.ok) {
      throw new Error(
        data.detail ||
        data.message ||
        `Server error (${response.status})`
      );
    }

    if (!data.download) {
      throw new Error("Server did not return the enhanced file.");
    }

    download.href = data.download;
    download.classList.remove("hidden");

    status.textContent = "✅ Enhancement complete!";
  } catch (error) {
    console.error(error);
    status.textContent = "❌ " + error.message;
  }

  btn.disabled = false;
};
