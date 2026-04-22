import {NextIntlClientProvider} from 'next-intl';
import "./globals.css";

type Props = {
  children: React.ReactNode;
};
 
export default async function RootLayout({children}: Props) {
  return (
    <html>
      <body>
        <NextIntlClientProvider>{children}</NextIntlClientProvider>
      </body>
    </html>
  );
}