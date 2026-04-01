import { t } from "../core/i18n.js";
import { applyLang } from "../core/dom.js";

export function setupHelpWidget() {
  const hwHTML = `
  <div class="hw-container">
    <button id="hwBtn" class="hw-btn"><i class="bi bi-question-circle-fill"></i> <span data-i18n="hwBtn">Help</span></button>
    <div id="hwBox" class="hw-box">
      <div class="hw-header">
        <span data-i18n="hwHeader">Leave us a message</span>
        <button id="hwClose" class="hw-close" aria-label="Close widget"><i class="bi bi-dash"></i></button>
      </div>
      <form class="hw-form" action="https://formsubmit.co/fatonyahmadfauzi@gmail.com" method="POST" enctype="multipart/form-data">
        <input type="hidden" name="_subject" value="Pesan Bantuan dari Pixiv OAuth Web">
        <input type="hidden" name="_next" value="https://pixiv-o-auth-token.vercel.app/contact?success=true">
        <input type="hidden" name="_captcha" value="true">
        <input type="hidden" name="_template" value="box">
  
        <div class="hw-group">
          <label data-i18n="hwName">Your Name</label>
          <input type="text" name="Nama_Anda" class="hw-input" required>
        </div>
        <div class="hw-group">
          <label data-i18n="hwEmail">Email address</label>
          <input type="email" name="email" class="hw-input" required>
        </div>
        <div class="hw-group">
          <label data-i18n="hwMessage">How can we help you?</label>
          <textarea name="Pesan" class="hw-input" required></textarea>
        </div>
        <div class="hw-group">
          <label class="hw-file-wrap"><span data-i18n="hwAttachment">Attachment</span> <div><i class="bi bi-paperclip"></i> <span data-i18n="hwAttachHint">Add up to 5 files</span></div></label>
          <div class="hw-custom-file">
    <label for="hwFile" class="hw-file-btn" data-i18n="hwChooseFile">Choose Files</label>
    <span id="hwFileName" class="hw-file-name" data-i18n="hwNoFile">No file chosen</span>
  </div>
  <input type="file" id="hwFile" name="attachment" accept="image/*,.pdf,.zip,.log,.txt" multiple style="display:none;">
        </div>
        <button type="submit" class="hw-submit" data-i18n="hwSubmit">Send</button>
      </form>
    </div>
  </div>`;
  
  if (
    "/404" !== window.location.pathname &&
    "/enable-javascript" !== window.location.pathname &&
    !document.body.classList.contains("page-not-found")
  ) {
    document.body.insertAdjacentHTML("beforeend", hwHTML);

    const hwBtn = document.getElementById("hwBtn"),
      hwBox = document.getElementById("hwBox"),
      hwClose = document.getElementById("hwClose");
      
    if (hwBtn && hwBox && hwClose) {
      hwBtn.addEventListener("click", () => {
        hwBox.classList.add("show");
        hwBtn.style.opacity = "0";
        hwBtn.style.pointerEvents = "none";
      });
      hwClose.addEventListener("click", (e) => {
        e.preventDefault();
        hwBox.classList.remove("show");
        hwBtn.style.opacity = "1";
        hwBtn.style.pointerEvents = "auto";
      });
    }
    
    // Make sure the newly injected HTML gets translated!
    applyLang();
    
    const hwFileEl = document.getElementById("hwFile"),
      hwFileNameEl = document.getElementById("hwFileName");
    if (hwFileEl && hwFileNameEl) {
      hwFileEl.addEventListener("change", function () {
        if (this.files && this.files.length > 0) {
          hwFileNameEl.textContent = Array.from(this.files).map((f) => f.name).join(", ");
          hwFileNameEl.style.color = "#2c374a";
        } else {
          hwFileNameEl.textContent = t("hwNoFile");
          hwFileNameEl.style.color = "#8a98b8";
        }
      });
    }
  }
}
