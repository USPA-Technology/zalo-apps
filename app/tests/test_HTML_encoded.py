import html
from bs4 import BeautifulSoup

# The given HTML-encoded string
encoded_string = '''&lt;div style&#x3D;&quot;color: rgb(30, 49, 80); font-size: 15px;&quot; title&#x3D;&quot;Header&quot;&gt;Kh&aacute;ch c&oacute; mua đệm nhưng bị xẹp l&uacute;n kh&ocirc;ng đều&lt;/div&gt;'''


description = '''&lt;div style&#x3D;&quot;color: rgb(30, 49, 80); font-size: 15px;&quot;&gt;Chị Tuyền Chị Tuyền kh&aacute;ch đại l&yacute; Kontum mua bộ 23037 bị loang m&agrave;u. Hỗ trợ giặt lần đầu v&agrave; đổi h&agrave;ng cho kh&aacute;ch (qua gọi điện t&igrave;m hiểu, kh&aacute;ch giặt lần đầu bằng sữa tắm) li&ecirc;n hệ kh&aacute;ch ng&agrave;y 15/3&lt;/div&gt;\n&lt;div style&#x3D;&quot;color: rgb(30, 49, 80); font-size: 15px;&quot;&gt;&nbsp;&lt;/div&gt;'''
# Step 1: Decode HTML entities
decoded_string = html.unescape(description)

# Step 2: Parse HTML to extract text
soup = BeautifulSoup(decoded_string, 'html.parser')
plain_text = soup.get_text()

# Output the result
print(plain_text)
