"use client";

import * as React from "react";
import { useRouter } from 'next/navigation';
import { FileUploadForm } from "@/components/file-upload-form";
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";

const WelcomePage = () => {
  const router = useRouter();

  React.useEffect(() => {
    // Retrieve token from localStorage (or any other storage)
    const token = localStorage.getItem('access_token');
    if (!token) {
      // If no token, redirect to login page
      router.push('/login');
    }
  }, [router]);
  //
  // return (
  //   <div className="flex min-h-screen flex-col items-center items-start gap-2 p-6">
  //     <h1>Welcome!</h1>
  //     <p>You are successfully logged in.</p>
  //   </div>
  // );

  return (
    <section className="container grid items-center gap-6 pb-8 pt-6 md:py-10">
      <div className="flex max-w-[980px] flex-col items-start gap-2">
        <h1 className="text-3xl font-extrabold leading-tight tracking-tighter md:text-4xl">
          Welcome!<br className="hidden sm:inline" />
        </h1>
        <p className="max-w-[700px] text-lg text-muted-foreground">
          Upload a file:</p>
      </div>
    <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>File Upload</CardTitle>
        </CardHeader>
        <CardContent>
          <FileUploadForm />
        </CardContent>
        <CardFooter>
          {/* Card footer */}
        </CardFooter>
      </Card>
    </section>
  );
};

export default WelcomePage;
