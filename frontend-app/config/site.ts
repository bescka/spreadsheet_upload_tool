export type SiteConfig = typeof siteConfig

export const siteConfig = {
  name: "Spreadsheet Uploader Tool",
  description:
    "A tool to upload and transform spreadsheet data",
  mainNav: [
    {
      title: "Home",
      href: "/",
    },
  ],
  links: {
    github: "https://github.com/bescka/spreadsheet_uploader",
    docs: "https://github.com/bescka/spreadsheet_uploader",
    login: "/login",
    register: "/register",
    uploader: "/uploader"
  },
}
