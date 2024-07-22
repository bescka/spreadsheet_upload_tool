"use client";

import * as React from "react";
import { useRouter } from 'next/navigation';
import { UserAuthForm } from "@/components/user-auth-form";
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";


const LoginPage = () => {
  const router = useRouter();
  const handleSuccess = (data: { access_token: string }) => {
    // Store token in localStorage (or any other storage)
    localStorage.setItem('access_token', data.access_token);
    // Navigate to the welcome page
    router.push('/uploader');
  };
  return (
    <div className="flex min-h-screen flex-col items-center items-start gap-2 p-6">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Login</CardTitle>
        </CardHeader>
        <CardContent>
          <UserAuthForm onSuccess={handleSuccess} />
        </CardContent>
        <CardFooter>
          {/* Card footer */}
        </CardFooter>
      </Card>
    </div>
  );
};

export default LoginPage;
