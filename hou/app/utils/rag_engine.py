import os
import requests
from flask import current_app
from app.models.qa import KnowledgeBase, UniversityFAQ, QAPromptTemplate
from openai import OpenAI
import numpy as np

class RAGEngine:
    def __init__(self):
        self.client = None
        
    def _get_client(self):
        if not self.client:
            self.client = OpenAI(
                api_key=current_app.config['DASHSCOPE_API_KEY'],
                base_url=current_app.config['LLM_BASE_URL']
            )
        return self.client

    def retrieve_from_rag(self, question, university_id=None):
        """
        RAG 检索逻辑（简易内存版）
        实际应结合向量数据库 (Milvus/Pinecone)
        """
        # 1. 查询相关的知识库片段 (这里假设 content_chunks 存储了文本)
        query = KnowledgeBase.query.filter_by(status=1)
        if university_id:
            query = query.filter_by(university_id=university_id)
        
        docs = query.all()
        relevant_context = ""
        for doc in docs:
            # 简单演示：前两个片段
            if doc.content_chunks:
                relevant_context += "\n".join(doc.content_chunks[:2])
                
        return relevant_context

    def call_llm(self, prompt, model=None):
        """
        调用 Qwen3 (通过 DashScope OpenAI 兼容接口)
        """
        client = self._get_client()
        try:
            response = client.chat.completions.create(
                model=model or current_app.config['LLM_MODEL'],
                messages=[
                    {"role": "system", "content": "你是一个高考志愿咨询专家。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            current_app.logger.error(f"LLM Call Failed: {str(e)}")
            return None

    def answer_with_fallback(self, question, university_id=None):
        """
        问答降级流程
        """
        # 1. 尝试 RAG + LLM
        context = self.retrieve_from_rag(question, university_id)
        if context:
            prompt = f"参考以下背景知识回答问题：\n{context}\n\n问题：{question}"
            answer = self.call_llm(prompt)
            if answer:
                return answer, True
        
        # 2. RAG 失败或无背景，尝试 FAQ 匹配
        faq_query = UniversityFAQ.query
        if university_id:
            faq_query = faq_query.filter_by(university_id=university_id)
        
        # 简单关键字匹配作为演示
        faq = faq_query.filter(UniversityFAQ.question.like(f"%{question[:10]}%")).first()
        if faq:
            return faq.answer, False
            
        # 3. 最终兜底
        return "很抱歉，我目前无法回答这个问题。您可以尝试通过『咨询列表』联系人工客服。", False

rag_engine = RAGEngine()
