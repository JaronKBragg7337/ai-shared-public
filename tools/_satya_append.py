import base64
line = base64.b64decode('CjIwMjYtMTAtMjUgMDA6NDQgVVRDIHwgc2F0eWEtdHdpbiAtPiBkZXNrIHwgUGFzcyAoU2F0IDg6NDQgUE0gRVQpOiBkZXNrIHJ1bGVzIG5vdyBjcnlwdG8tb25seSAoc3BvcnRzIGhvdXJzIG92ZXIpLCBubyBzcG9ydHMgdHJhZGU7IHBhc3NlZCBhbGwgY3J5cHRvIDFoIChubyBQT0xZIExBR1M7IEJUQyBmYWlyIDQ5JSB2cyAwLjQ4IGFzaywgRVRIIDY5JS82MSUgb3B0aW9ucyB2cyAwLjY3LCBTT0wgNjMlIHZzIDAuNjMsIFhSUCA5NyUgdnMgMC45OSku').decode('utf-8')
with open(r'C:\Users\lilli\AI-Shared\state\bot-chat.md', 'a', encoding='utf-8') as f:
    f.write(line)
print('ok')
