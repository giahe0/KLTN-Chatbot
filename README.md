# chatgpt-retrieval

Script đơn giản để sử dụng data của riêng bạn

xem vd ở đây [YouTube Video](https://youtu.be/ab8X6oLsIlU).

## Cài đặt 

Install [Langchain](https://github.com/hwchase17/langchain) và các gói cần thiết.
```
pip install langchain openai chromadb tiktoken unstructured
```
Sửa lại file `constants.py.default` thành `constants.py` sau khi chèn APIkey ở [OpenAI API key](https://platform.openai.com/account/api-keys).

Chỉnh sửa dữ liệu của cá nhân bạn ở đây `data/data.txt`.

## VD cách dùng
Test reading `data/data.txt` file.
```
> python chatgpt.py "what is my dog's name"
Your dog's name is Sunny.
```

Test reading `data/cat.pdf` file.
```
> python chatgpt.py "what is my cat's name"
Your cat's name is Muffy.
```
