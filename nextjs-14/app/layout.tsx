import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import dynamic from "next/dynamic";
import Header from "./components/common/module/header";

const ReduxProvider = dynamic(() => import("@/redux/redux-provider"), {
  ssr: false
});

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Create Next App",
  description: "Generated by create next app",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
      <Header/>
      <div className="mt-100">
        <ReduxProvider > {children}</ReduxProvider>
        </div>
      </body>
    </html>
  );
}