"use client";

import { useTranslations } from "next-intl";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function HomePage() {
  const router = useRouter();
  const t = useTranslations("HomePage");

  const changeLocale = (locale: string) => {
    document.cookie = `locale=${locale}; path=/`;
    router.refresh();
  };

  const applyTheme = (theme: string) => {
    document.documentElement.classList.remove("light", "dark");
    document.documentElement.classList.add(theme);
  };

  const changeTheme = (theme: string) => {
    document.cookie = `theme=${theme}; path=/`;
    applyTheme(theme);
  };

  useEffect(() => {
    const cookieTheme = document.cookie
      .split("; ")
      .find((row) => row.startsWith("theme="))
      ?.split("=")[1];

    applyTheme(cookieTheme || "light");
  }, []);

  return (
    <div>
      <h1>{t("title")}</h1>

      {/* 🌍 locale */}
      <button onClick={() => changeLocale("en")}>EN</button>
      <button onClick={() => changeLocale("pt")}>PT</button>

      {/* 🎨 theme */}
      <button onClick={() => changeTheme("light")}>Light</button>
      <button onClick={() => changeTheme("dark")}>Dark</button>
    </div>
  );
}
