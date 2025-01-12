from django.utils import timezone
from datetime import timedelta
from .models import Question, Answer, Comment
from django.http import JsonResponse
import requests
import dashscope
from typing import Dict, List, Any
from django.core.cache import cache
import logging

class DataPack:
    @staticmethod
    def get_data_for_date(model, date):
        """获取某个模型在指定日期的数据"""
        return model.objects.filter(create_date=date)
    
    @staticmethod
    def get_data_for_range(model, start_datetime, end_datetime):
        """获取某个模型在指定时间范围内的数据"""
        return model.objects.filter(create_date__range=(start_datetime, end_datetime))

    def get_data_by_time(self, request, date_range=False):
        today = timezone.now().date()
        print('today:', today)
        if date_range:
            # 需要范围查询时，直接用start_date和end_date
            start_of_day = today  
            end_of_day = today  
            questions = self.get_data_for_range(Question, start_of_day, end_of_day)
            answers = self.get_data_for_range(Answer, start_of_day, end_of_day)
            comments = self.get_data_for_range(Comment, start_of_day, end_of_day)
        else:
            questions = self.get_data_for_date(Question, today)
            print(questions)
            answers = self.get_data_for_date(Answer, today)
            print(answers)
            comments = self.get_data_for_date(Comment, today)
            print(comments)

        return self.format_data(questions, answers, comments)

    @staticmethod
    def format_data(questions, answers, comments):
        """格式化数据"""
        questions_data = [{"id": q.id, "title": q.title, "content": q.content, "create_date": q.create_date} for q in questions]
        answers_data = [{"id": a.id, "question_id": a.question.id, "content": a.content, "create_date": a.create_date} for a in answers]
        comments_data = [{"id": c.id, "answer_id": c.answer.id, "content": c.content, "create_date": c.create_date} for c in comments]

        return {"questions": questions_data, "answers": answers_data, "comments": comments_data}



class KnowledgeBasedQA:
    def __init__(self):
        self.data_pack = DataPack()
        self.API_KEY = 'sk-29d11309d0ff4c468ee45dcce16e2806'
        self.conversation_history = {
            'user': [],
            'ai': []
        }
        self.max_history = 5  # 保留最近5轮对话
        self.logger = logging.getLogger(__name__)

    def _get_knowledge_base(self) -> str:
        """获取并格式化知识库内容"""
        try:
            # 获取今日数据
            print('12')
            today_data = self.data_pack.get_data_by_time(None, date_range=False)
            print('34')
            # 构建知识库文本
            knowledge_text = "系统知识库内容：\n"
            
            # 添加问题
            for q in today_data['questions']:
                knowledge_text += f"问题ID[{q['id']}]: {q['title']}\n问题内容: {q['content']}\n\n"
            
            # 添加回答
            for a in today_data['answers']:
                knowledge_text += f"问题[{a['question_id']}]的回答: {a['content']}\n\n"
            
            # 添加评论
            for c in today_data['comments']:
                knowledge_text += f"回答[{c['answer_id']}]的评论: {c['content']}\n\n"
            print('knowledge_text: ', knowledge_text)
            return knowledge_text
        
        except Exception as e:
            self.logger.error(f"Error getting knowledge base: {str(e)}")
            return ""

    def _update_conversation_history(self, user_input: str, ai_response: str):
        """更新对话历史"""
        self.conversation_history['user'].append(user_input)
        self.conversation_history['ai'].append(ai_response)
        
        # 保持历史记录在限定范围内
        if len(self.conversation_history['user']) > self.max_history:
            self.conversation_history['user'] = self.conversation_history['user'][-self.max_history:]
            self.conversation_history['ai'] = self.conversation_history['ai'][-self.max_history:]

    def get_response(self, user_query: str) -> Dict[str, Any]:
        """获取AI回答"""
        try:
            # 获取知识库内容
            knowledge_base = self._get_knowledge_base()
            
            # 构建完整提示词
            prompt = f"""请基于以下知识库内容和上下文回答用户问题。如果问题与知识库内容相关，请优先使用知识库中的信息。
            如果问题与知识库无关，可以基于你的知识回答。

{knowledge_base}

用户问题: {user_query}

请给出清晰、准确的回答。"""

            # 构建消息历史
            messages = []
            for user_msg, ai_msg in zip(self.conversation_history['user'], 
                                      self.conversation_history['ai']):
                messages.extend([
                    {"role":"system", "content": ""},
                    {"role": "user", "content": user_msg},
                    {"role": "assistant", "content": ai_msg}
                ])
            messages.append({"role":"system", "content": "回答以纯文本形式回答，不要用Markdown"})
            messages.append({"role": "user", "content": prompt})
            print(111)
            print('messages:',messages)
            # 调用API
            dashscope.api_key = self.API_KEY
            response = dashscope.Generation.call(
                model="qwen-turbo",
                messages=messages,
                result_format='message'
            )

            ai_response = response.output.choices[0].message.content
            print(ai_response)
            # 更新对话历史
            self._update_conversation_history(user_query, ai_response)

            return {
                "success": True,
                "response": ai_response,
                "has_knowledge_base": bool(knowledge_base.strip())
            }

        except Exception as e:
            self.logger.error(f"Error in get_response: {str(e)}")
            return {
                "success": False,
                "error": "Failed to get AI response",
                "details": str(e)
            }