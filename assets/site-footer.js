(function () {
  const footerLinks = [
    {
      key: "patreon",
      label: "Patreon",
      icon: "P",
      href: "https://www.patreon.com/wlop",
      title: {
        vi: "Trang Patreon: Đăng ký hàng tháng, hỗ trợ thẻ tín dụng, PayPal và thanh toán quốc tế.",
        zh: "Patreon 网站：按月订阅，支持信用卡、PayPal 等国际支付。"
      }
    },
    {
      key: "gumroad",
      label: "Gumroad",
      icon: "G",
      href: "https://wlop.gumroad.com/",
      title: {
        vi: "Trang Gumroad: Mua trực tiếp tác phẩm, hỗ trợ thẻ tín dụng, PayPal và thanh toán quốc tế.",
        zh: "Gumroad 网站：直接购买作品，支持信用卡、PayPal 等国际支付。"
      }
    },
    { divider: true },
    {
      key: "huotan",
      label: "货摊网",
      icon: "货",
      href: "https://wlop.huotan.net/",
      title: {
        vi: "Trang HuoTan: Mua trực tiếp tác phẩm, hỗ trợ WeChat Pay và Alipay.",
        zh: "货摊网：直接购买作品，支持微信支付和支付宝。"
      }
    },
    {
      key: "azz",
      label: "爱赞助",
      icon: "爱",
      href: "https://azz.net/wlop",
      title: {
        vi: "Trang AZZ: Đăng ký hàng tháng, hỗ trợ WeChat Pay và Alipay.",
        zh: "爱赞助网站：按月订阅，支持微信支付和支付宝。"
      }
    }
  ];

  const linkMap = new Map(footerLinks.filter((item) => item.key).map((item) => [item.key, item]));
  const copyrightText = {
    vi: "© WLOP. Toàn bộ nội dung và bản quyền liên quan trên trang web này thuộc về WLOP. Mọi hành vi sao chép, tái bản, cải biên hoặc sử dụng cho mục đích thương mại khi chưa được phép đều bị nghiêm cấm. Bảo lưu mọi quyền.",
    zh: "© WLOP。本网站全部内容及相关权益归 WLOP 所有，未经授权不得转载、复制、改编或用于商业用途。保留所有权利。"
  };
  const contactText = {
    vi: "Liên hệ:",
    zh: "联系我："
  };
  const contactEmail = "ZYDNQ5010@gmail.com";

  function getCurrentFooterLanguage() {
    const htmlLang = document.documentElement.lang || "";
    if (/^vi\b/i.test(htmlLang)) return "vi";
    return "zh";
  }

  function applyFooterLanguage() {
    const lang = getCurrentFooterLanguage();
    document.querySelectorAll(".cloudinsect-copyright").forEach((copyright) => {
      copyright.textContent = copyrightText[lang] || copyrightText.zh;
    });

    document.querySelectorAll(".cloudinsect-contact-label").forEach((label) => {
      label.textContent = contactText[lang] || contactText.zh;
    });

    document.querySelectorAll(".cloudinsect-footer-link[data-footer-key]").forEach((link) => {
      const item = linkMap.get(link.dataset.footerKey);
      if (!item) return;
      const title = item.title[lang] || item.title.zh;
      link.dataset.tooltip = title;
      link.setAttribute("aria-label", `${item.label}: ${title}`);
    });
  }

  function createFooter() {
    const footer = document.createElement("footer");
    footer.className = "cloudinsect-footer";
    footer.setAttribute("aria-label", "Site footer");

    const inner = document.createElement("div");
    inner.className = "cloudinsect-footer-inner";

    const copyright = document.createElement("p");
    copyright.className = "cloudinsect-copyright";
    copyright.textContent = copyrightText[getCurrentFooterLanguage()] || copyrightText.zh;

    const contact = document.createElement("p");
    contact.className = "cloudinsect-contact";

    const contactLabel = document.createElement("span");
    contactLabel.className = "cloudinsect-contact-label";
    contactLabel.textContent = contactText[getCurrentFooterLanguage()] || contactText.zh;

    const contactLink = document.createElement("a");
    contactLink.className = "cloudinsect-contact-email";
    contactLink.href = `mailto:${contactEmail}`;
    contactLink.textContent = contactEmail;

    contact.append(contactLabel, " ", contactLink);

    const links = document.createElement("nav");
    links.className = "cloudinsect-footer-links";
    links.setAttribute("aria-label", "Creator links");

    footerLinks.forEach((item) => {
      if (item.divider) {
        const divider = document.createElement("span");
        divider.className = "cloudinsect-footer-divider";
        divider.setAttribute("aria-hidden", "true");
        links.appendChild(divider);
        return;
      }

      const link = document.createElement("a");
      link.className = "cloudinsect-footer-link";
      link.href = item.href;
      link.dataset.footerKey = item.key;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.textContent = item.icon;

      links.appendChild(link);
    });

    inner.append(copyright, contact, links);
    footer.appendChild(inner);
    return footer;
  }

  function appendFooter(target) {
    if (!target || target.querySelector(".cloudinsect-footer")) return;
    target.appendChild(createFooter());
    applyFooterLanguage();
  }

  function initFooter() {
    const site = document.querySelector(".site");
    if (site) {
      appendFooter(site);
      return;
    }

    const comics = Array.from(document.querySelectorAll(".comic"));
    if (comics.length) {
      comics.forEach(appendFooter);
      return;
    }

    appendFooter(document.body);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initFooter, { once: true });
  } else {
    initFooter();
  }

  document.addEventListener("click", (event) => {
    const languageButton = event.target && event.target.closest
      ? event.target.closest(".lang-option")
      : null;
    if (!languageButton) return;
    window.setTimeout(applyFooterLanguage, 0);
  });
}());
