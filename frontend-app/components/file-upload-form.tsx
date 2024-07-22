"use client";

import * as React from "react";
import { useForm, SubmitHandler, FormProvider } from "react-hook-form";
import { Form, FormField, FormItem, FormLabel, FormControl, FormDescription, FormMessage } from "@/components/ui/form";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardFooter, CardTitle } from "@/components/ui/card";
import Papa from 'papaparse';
import axios from "axios";

interface FileUploadFormProps extends React.HTMLAttributes<HTMLDivElement> {}

interface FileUploadFormValues {
  file: FileList;
}

export function FileUploadForm({ className, ...props }: FileUploadFormProps) {
  const form = useForm<FileUploadFormValues>({
    defaultValues: {
      file: null,
    },
  });
  const [isLoading, setIsLoading] = React.useState<boolean>(false);
  const [message, setMessage] = React.useState<string | null>(null);
  const [csvData, setCsvData] = React.useState<any[]>([]);
  const [showPreview, setShowPreview] = React.useState<boolean>(false);

  const onSubmit: SubmitHandler<FileUploadFormValues> = async () => {
    if (!csvData.length) {
      setMessage("No CSV data to upload.");
      return;
    }

    setIsLoading(true);
    setMessage(null);

    const formData = new FormData();
    formData.append("file", new Blob([Papa.unparse(csvData)], { type: 'text/csv' }), 'upload.csv');

    try {
      const response = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/fileupload/`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
      });

      setMessage("File uploaded successfully!");
      setShowPreview(false);
    } catch (error) {
      console.error(error);
      setMessage("File upload failed. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && (file.type === 'text/csv' || file.name.endsWith('.csv'))) {
      form.setValue("file", event.target.files);
      setMessage(null);
    }
  };

  const handlePreview = () => {
    const file = form.getValues("file")?.[0];
    if (file && (file.type === 'text/csv' || file.name.endsWith('.csv'))) {
      Papa.parse(file, {
        header: true,
        complete: (results) => {
          setCsvData(results.data);
          setShowPreview(true);
        },
        error: (error) => {
          console.error("Error parsing CSV:", error);
          setMessage("Error parsing CSV file.");
        },
      });
    } else {
      setMessage("Please select a CSV file.");
    }
  };

  const handleCancel = () => {
    setShowPreview(false);
    setCsvData([]);
    form.reset();
  };

  return (
    <div className={className} {...props}>
      <FormProvider {...form}>
        <form className="space-y-4">
          <FormField
            name="file"
            control={form.control}
            render={({ field }) => (
              <FormItem>
                <FormLabel>File</FormLabel>
                <FormControl>
                  <Input
                    type="file"
                    onChange={(e) => {
                      field.onChange(e.target.files);
                      handleFileChange(e);
                    }}
                  />
                </FormControl>
                <FormDescription>Upload a CSV file</FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />
          <Button type="button" onClick={handlePreview}>
            Preview
          </Button>
        </form>
        {message && <p>{message}</p>}
      </FormProvider>

      {showPreview && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex justify-center items-center">
          <Card className="w-full max-w-4xl mx-auto max-h-[80vh] overflow-y-auto">
            <CardHeader>
              <CardTitle>CSV Preview</CardTitle>
            </CardHeader>
            <CardContent>
              {csvData.length > 0 && (
                <div className="overflow-auto">
                  <table className="w-full">
                    <thead>
                      <tr>
                        {Object.keys(csvData[0]).map((key) => (
                          <th key={key} className="border px-4 py-2">{key}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {csvData.map((row, index) => (
                        <tr key={index}>
                          {Object.values(row).map((value, i) => (
                            <td key={i} className="border px-4 py-2">{value as string}</td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </CardContent>
            <CardFooter className="flex justify-end space-x-4">
              <Button variant="outline" onClick={handleCancel}>Cancel</Button>
              <Button onClick={form.handleSubmit(onSubmit)} disabled={isLoading}>
                {isLoading && <span className="spinner mr-2" />} Upload
              </Button>
            </CardFooter>
          </Card>
        </div>
      )}
    </div>
  );
}


// "use client";
//
// import * as React from "react";
// import { useForm, SubmitHandler, FormProvider } from "react-hook-form";
// import { Form, FormField, FormItem, FormLabel, FormControl, FormDescription, FormMessage } from "@/components/ui/form";
// import { Button } from "@/components/ui/button";
// import { Input } from "@/components/ui/input";
// import { Card, CardContent, CardHeader, CardFooter, CardTitle } from "@/components/ui/card";
// import Papa from 'papaparse';
// import axios from "axios";
//
// interface FileUploadFormProps extends React.HTMLAttributes<HTMLDivElement> {}
//
// interface FileUploadFormValues {
//   file: FileList;
// }
//
// export function FileUploadForm({ className, ...props }: FileUploadFormProps) {
//   const form = useForm<FileUploadFormValues>({
//     defaultValues: {
//       file: null,
//     },
//   });
//   const [isLoading, setIsLoading] = React.useState<boolean>(false);
//   const [message, setMessage] = React.useState<string | null>(null);
//   const [csvData, setCsvData] = React.useState<any[]>([]);
//   const [showPreview, setShowPreview] = React.useState<boolean>(false);
//
//   const onSubmit: SubmitHandler<FileUploadFormValues> = async () => {
//     if (!csvData.length) {
//       setMessage("No CSV data to upload.");
//       return;
//     }
//
//     setIsLoading(true);
//     setMessage(null);
//
//     const formData = new FormData();
//     formData.append("file", new Blob([Papa.unparse(csvData)], { type: 'text/csv' }), 'upload.csv');
//
//     try {
//       const response = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/fileupload/`, formData, {
//         headers: {
//           "Content-Type": "multipart/form-data",
//           Authorization: `Bearer ${localStorage.getItem('access_token')}`,
//         },
//       });
//
//       setMessage("File uploaded successfully!");
//       setShowPreview(false);
//     } catch (error) {
//       console.error(error);
//       setMessage("File upload failed. Please try again.");
//     } finally {
//       setIsLoading(false);
//     }
//   };
//
//   const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
//     const file = event.target.files?.[0];
//     if (file && (file.type === 'text/csv' || file.name.endsWith('.csv'))) {
//       Papa.parse(file, {
//         header: true,
//         complete: (results) => {
//           setCsvData(results.data);
//           setShowPreview(true);
//         },
//         error: (error) => {
//           console.error("Error parsing CSV:", error);
//           setMessage("Error parsing CSV file.");
//         },
//       });
//     }
//   };
//
//   const handleCancel = () => {
//     setShowPreview(false);
//     setCsvData([]);
//     form.reset();
//   };
//
//   return (
//     <div className={className} {...props}>
//       <FormProvider {...form}>
//         <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
//           <FormField
//             name="file"
//             control={form.control}
//             render={({ field }) => (
//               <FormItem>
//                 <FormLabel>File</FormLabel>
//                 <FormControl>
//                   <Input
//                     type="file"
//                     onChange={(e) => {
//                       field.onChange(e.target.files);
//                       handleFileChange(e);
//                     }}
//                   />
//                 </FormControl>
//                 <FormDescription>Upload a CSV file</FormDescription>
//                 <FormMessage />
//               </FormItem>
//             )}
//           />
//         </form>
//         {message && <p>{message}</p>}
//       </FormProvider>
//
//       {showPreview && (
//         <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex justify-center items-center">
//           <Card className="w-full max-w-4xl mx-auto">
//             <CardHeader>
//               <CardTitle>CSV Preview</CardTitle>
//             </CardHeader>
//             <CardContent>
//               {csvData.length > 0 && (
//                 <table className="w-full">
//                   <thead>
//                     <tr>
//                       {Object.keys(csvData[0]).map((key) => (
//                         <th key={key} className="border px-4 py-2">{key}</th>
//                       ))}
//                     </tr>
//                   </thead>
//                   <tbody>
//                     {csvData.map((row, index) => (
//                       <tr key={index}>
//                         {Object.values(row).map((value, i) => (
//                           <td key={i} className="border px-4 py-2">{value as string}</td>
//                         ))}
//                       </tr>
//                     ))}
//                   </tbody>
//                 </table>
//               )}
//             </CardContent>
//             <CardFooter className="flex justify-end space-x-4">
//               <Button variant="outline" onClick={handleCancel}>Cancel</Button>
//               <Button onClick={form.handleSubmit(onSubmit)} disabled={isLoading}>
//                 {isLoading && <span className="spinner mr-2" />} Upload
//               </Button>
//             </CardFooter>
//           </Card>
//         </div>
//       )}
//     </div>
//   );
// }
// "use client";
//
// import * as React from "react";
// import { useForm, SubmitHandler, FormProvider } from "react-hook-form";
// import { Form, FormField, FormItem, FormLabel, FormControl, FormDescription, FormMessage } from "@/components/ui/form";
// import { Button } from "@/components/ui/button";
// import { Input } from "@/components/ui/input";
// import axios from "axios";
//
// interface FileUploadFormProps extends React.HTMLAttributes<HTMLDivElement> {}
//
// interface FileUploadFormValues {
//   file: FileList;
// }
//
// export function FileUploadForm({ className, ...props }: FileUploadFormProps) {
//   const form = useForm<FileUploadFormValues>({
//     defaultValues: {
//       file: null,
//     },
//   });
//   const [isLoading, setIsLoading] = React.useState<boolean>(false);
//   const [message, setMessage] = React.useState<string | null>(null);
//
//   const onSubmit: SubmitHandler<FileUploadFormValues> = async (data) => {
//     setIsLoading(true);
//     setMessage(null);
//
//     const file = data.file?.[0];
//
//     // Check if the file is a CSV
//     if (!file || (file.type !== 'text/csv' && !file.name.endsWith('.csv'))) {
//       setMessage("Only CSV files are allowed.");
//       setIsLoading(false);
//       return;
//     }
//
//     const formData = new FormData();
//     formData.append("file", file);
//
//     try {
//       const response = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/fileupload/`, formData, {
//         headers: {
//           "Content-Type": "multipart/form-data",
//           Authorization: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0aW5nQHRlc3RpbmcuY29tIiwiZXhwIjoxNzIxNjQ3MDU5fQ.Kax0666msLP7LBn4QtJBdRPNtO3tuWtYVVw95-ZZHxk` //${localStorage.getItem('access_token')}`,
//         },
//       });
//
//       setMessage("File uploaded successfully!");
//     } catch (error) {
//       console.error(error);
//       setMessage("File upload failed. Please try again.");
//     } finally {
//       setIsLoading(false);
//     }
//   };
//
//   return (
//     <div className={className} {...props}>
//       <FormProvider {...form}>
//         <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
//           <FormField
//             name="file"
//             control={form.control}
//             render={({ field }) => (
//               <FormItem>
//                 <FormLabel>File</FormLabel>
//                 <FormControl>
//                   <Input
//                     type="file"
//                     onChange={(e) => field.onChange(e.target.files)}
//                   />
//                 </FormControl>
//                 <FormDescription>Upload a CSV file</FormDescription>
//                 <FormMessage />
//               </FormItem>
//             )}
//           />
//           <Button type="submit" disabled={isLoading}>
//             {isLoading && <span className="spinner mr-2" />} Upload File
//           </Button>
//         </form>
//         {message && <p>{message}</p>}
//       </FormProvider>
//     </div>
//   );
// }
