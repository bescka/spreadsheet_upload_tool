"use client";

import * as React from "react";
import { useForm, SubmitHandler, FormProvider } from "react-hook-form";
import {
  Form,
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormDescription,
  FormMessage,
} from "@/components/ui/form";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface UserAuthFormProps extends React.HTMLAttributes<HTMLDivElement> {}

interface LoginFormValues {
  email: string;
}

export function UserAuthForm({ className, ...props }: UserAuthFormProps) {
  const form = useForm<LoginFormValues>();
  const [isLoading, setIsLoading] = React.useState<boolean>(false);

  const onSubmit: SubmitHandler<LoginFormValues> = async (data) => {
    console.log(data);
    setIsLoading(true);

    // Simulate login logic
    setTimeout(() => {
      setIsLoading(false);
    }, 3000);
  };

  return (
    <div className={className} {...props}>
      <FormProvider {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
          <FormField
            name="email"
            control={form.control}
            render={({ field }) => (
              <FormItem>
                <FormLabel>Email</FormLabel>
                <FormControl>
                  <Input
                    type="email"
                    placeholder="name@example.com"
                    {...field}
                  />
                </FormControl>
                <FormDescription>Enter your email address</FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />
          <Button type="submit" disabled={isLoading}>
            {isLoading && <span className="spinner mr-2" />} Sign In with Email
          </Button>
        </form>
      </FormProvider>
    </div>
  );
}
