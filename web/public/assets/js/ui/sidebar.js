export function setupMobileSidebar() {
  const menuToggle = document.getElementById("menuToggle"),
    sidebarOverlay = document.getElementById("sidebarOverlay"),
    navLinksContainer =
      document.querySelector(".nav-links") ||
      document.querySelector(".tutorial-docs-actions");
      
  if (menuToggle && sidebarOverlay && navLinksContainer) {
    function toggleSidebar() {
      navLinksContainer.classList.toggle("open");
      sidebarOverlay.classList.toggle("active");
      document.body.style.overflow = sidebarOverlay.classList.contains("active") ? "hidden" : "";
    }
    
    menuToggle.addEventListener("click", toggleSidebar);
    sidebarOverlay.addEventListener("click", toggleSidebar);
    
    navLinksContainer.querySelectorAll(".close-sidebar").forEach((btn) => 
        btn.addEventListener("click", toggleSidebar)
    );
    
    navLinksContainer.querySelectorAll("a:not(.sidebar-brand)").forEach((link) => {
      link.addEventListener("click", () => {
        navLinksContainer.classList.remove("open");
        sidebarOverlay.classList.remove("active");
        document.body.style.overflow = "";
      });
    });
  }
}
