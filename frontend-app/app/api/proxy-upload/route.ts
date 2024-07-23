import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  const formData = await req.formData();

  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/fileupload/`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${formData.get('access_token')}`,
      },
      body: formData,
    });

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}
