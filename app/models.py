from pydantic import BaseModel
from typing import Optional, Dict, List, Union
import json

# class UserBase(BaseModel):
#     user_id: str
    

# class UserZaloOA(UserBase):
#     user_zalo_id: str




template_message = """ {
    "recipient": {
        "user_id": "465869129535977702"
    },
    "message": {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "promotion",
                "elements": [
                    {
                        "attachment_id":"aERC3A0iYGgQxim8fYIK6fxzsXkaFfq7ZFRB3RCyZH6RyziRis3RNydebK3iSPCJX_cJ3k1nW1EQufjN_pUL1f6Ypq3rTef5nxp6H_HnXKFDiyD5y762HS-baqRpQe5FdA376lTfq1sRyPr8ypd74ecbaLyA-tGmuJ-97W",
                        "type": "banner"
                    },
                    {
                        "type": "header",
                        "content": "💥💥Ưu đãi thành viên Platinum💥💥"
                    },
                    {
                        "type": "text",
                        "align": "left",
                        "content": "Ưu đãi dành riêng cho khách hàng Nguyen Van A hạng thẻ Platinum<br>Voucher trị giá 150$"
                    },
                    {
                        "type": "table",
                        "content": [
                            {
                                "value": "VC09279222",
                                "key": "Voucher"
                            },
                            {
                                "value": "30/12/2023",
                                "key": "Hạn sử dụng"
                            }
                        ]
                    },
                    {
                        "type": "text",
                        "align": "center",
                        "content": "Áp dụng tất cả cửa hàng trên toàn quốc"
                    }
                ],
                "buttons": [
                    {
                        "title": "Tham khảo chương trình",
                        "image_icon": "",
                        "type": "oa.open.url", 
                        "payload": { 
                           "url": "https://oa.zalo.me/home" 
                                   }
                        },
                        {
                        "title": "Liên hệ chăm sóc viên",
                        "image_icon": "aeqg9SYn3nIUYYeWohGI1fYRF3V9f0GHceig8Ckq4WQVcpmWb-9SL8JLPt-6gX0QbTCfSuQv40UEst1imAm53CwFPsQ1jq9MsOnlQe6rIrZOYcrlWBTAKy_UQsV9vnfGozCuOvFfIbN5rcXddFKM4sSYVM0D50I9eWy3",
                        "type": "oa.query.hide",
                        "payload": "#tuvan"
                        
                    }
                ]
            }
            }
        }
    } """


template_message_json = json.loads(template_message)
print(template_message_json)


