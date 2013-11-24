call "C:\Program Files\Microsoft Visual Studio 10.0\VC\bin\vcvars32.bat"
"C:\Program Files\Microsoft Visual Studio 10.0\VC\bin\cl.exe" /analyze:only /analyze:quiet /analyze:log %2 /w /I%1 %3
