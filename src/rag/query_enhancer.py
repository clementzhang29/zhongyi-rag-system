import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

INTENT_PROMPT = ChatPromptTemplate.from_messages([("system", """你是一个查询意图分析器。分析用户关于中医国学的问题，输出JSON：
{
  "intent": "概念解释|实践方法|比较辨析|原文查找|养生建议|其他",
  "keywords": ["关键词1","关键词2"],
  "rewritten_query": "补全后的完整问题",
  "need_vernacular": true/false
}"""), ("human", "{question}")])

class QueryEnhancer:
    def __init__(self, config: dict):
        self.llm = ChatOpenAI(
            api_key=config['llm']['api_key'],
            base_url=config['llm']['base_url'],
            model=config['llm']['model'],
            temperature=0.1
        )
        self.chain = INTENT_PROMPT | self.llm | StrOutputParser()

    def enhance(self, question: str) -> dict:
        try:
            result = self.chain.invoke({"question": question})
            result = result.strip()
            if result.startswith('`'): result = result.split('\n',1)[1].rsplit('\n',1)[0]
            return json.loads(result)
        except:
            return {
                "intent": "其他",
                "keywords": question,
                "rewritten_query": question,
                "need_vernacular": False
            }
