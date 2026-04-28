from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi

prompt = PromptTemplate.from_template(
    "请将{text}翻译成英文")
model = Tongyi(model="qwen3-max")

chain = prompt | model
print(type( chain)) # <class 'langchain_core.runnables.base.RunnableSequence'>
'''
1. prompt | model
   ↓
2. 生成 RunnableSequence (这只是一个链对象，还没执行)
   ↓
3. 调用 chain.invoke() (执行这个链)
   ↓
4. 链内部执行 model.invoke()
   ↓
5. 模型返回 AIMessage (这就是最终输出)
'''