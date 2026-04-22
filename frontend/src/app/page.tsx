"use client";

import { useTranslations } from "next-intl";
import { useRouter } from "next/navigation";

export default function HomePage() {
  const router = useRouter();
  const t = useTranslations("HomePage");

  const changeLocale = (locale: string) => {
    document.cookie = `locale=${locale}; path=/`;
    router.refresh();
  };

  return (
    <>
      <h1>{t("title")}</h1>
      <button onClick={() => changeLocale("en")}>EN</button>
      <button onClick={() => changeLocale("pt")}>PT</button>
    </>
  );
}
