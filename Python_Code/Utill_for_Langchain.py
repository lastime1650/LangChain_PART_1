from typing import Optional, List, Any, Dict

from langchain.llms.ollama import Ollama # ollama LLM모델
from langchain.memory import ConversationBufferMemory
from langchain.chains.llm import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain.schema import SystemMessage, HumanMessage, AIMessage


class LLM_Manager():
    def __init__(self):
        self.Chains = {}
        '''
            ConversationID 는 딕셔너리 Key가 되면서도, 이전 대화를 기록하는 문자열로 쓰임
        '''
    '''
        모델 지정 
    '''
    def Init_Select_Model(self, ConversationID:str, Model:Any)->bool:
        if (self.Check_exists_ConversationID(ConversationID)):
            return False # 이미 존재하면 실패

        dictionary = {
            "Model":Model,
            "Conversation_Memory_inst":None,
            'Prompt':None,
            'Chain':None
        }

        self.Chains[ConversationID] = dictionary
        return True


    '''
        메모리 관련
    '''
    def Init_Conversation_Memory(self, ConversationID:str, return_messages:bool)->bool:
        if( not self.Check_exists_ConversationID(ConversationID) ):
            return False # 이미 존재하지 않으면 실패
        self.Chains[ConversationID]["Conversation_Memory_inst"] = ConversationBufferMemory( memory_key=ConversationID, return_messages=return_messages)
        return True

    def Conversation_Memory_add_SystemMessage(self, ConversationID:str, Input:str )->bool:
        if (not self.Check_exists_ConversationID(ConversationID)):
            return False  # 이미 존재하지 않으면 실패

        if (not self.Chains[ConversationID]["Conversation_Memory_inst"]):
            return False # 이미 존재하지 않으면 실패

        self.Chains[ConversationID]["Conversation_Memory_inst"].chat_memory.add_message(SystemMessage(content=Input))
        return True

    def Conversation_Memory_add_userMessage(self, ConversationID:str, Input:str )->bool:
        if (not self.Check_exists_ConversationID(ConversationID)):
            return False  # 이미 존재하지 않으면 실패

        if (not self.Chains[ConversationID]["Conversation_Memory_inst"]):
            return False # 이미 존재하지 않으면 실패

        self.Chains[ConversationID]["Conversation_Memory_inst"].chat_memory.add_user_message(Input)
        return True
    def Conversation_Memory_add_aiMessage(self, ConversationID:str, Input:str )->bool:
        if (not self.Check_exists_ConversationID(ConversationID)):
            return False  # 이미 존재하지 않으면 실패

        if (not self.Chains[ConversationID]["Conversation_Memory_inst"]):
            return False # 이미 존재하지 않으면 실패

        self.Chains[ConversationID]["Conversation_Memory_inst"].chat_memory.add_ai_message(Input)

        return True


    '''
        Template 관련
    '''
    def Set_Prompt(self, ConversationID:str, Prompt_System_Message:str)->bool:
        if (not self.Check_exists_ConversationID(ConversationID)):
            return False  # 이미 존재하지 않으면 실패

        # MessagesPlaceholder 덕분에 Template에 따로 "이전 대화 기록"추가하지 않고, 변수로 저장하여 기억함.
        Prompt = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template('''
                System: '''+Prompt_System_Message+'''
                Human say: {input}
                AI say
                '''),
                HumanMessagePromptTemplate.from_template("{input}"),
                MessagesPlaceholder(variable_name=ConversationID)
            ]
        )
        self.Chains[ConversationID]['Prompt'] = Prompt

    '''
        LLM 체인 생성
    '''
    def Set_Chain(self, ConversationID:str)->bool:
        if (not self.Check_exists_ConversationID(ConversationID)):
            return False  # 이미 존재하지 않으면 실패

        if (not self.Chains[ConversationID]["Model"]):
            return False # 이미 존재하지 않으면 실패

        if (not self.Chains[ConversationID]["Prompt"]):
            return False # 이미 존재하지 않으면 실패

        if (not self.Chains[ConversationID]["Conversation_Memory_inst"]):
            self.Chains[ConversationID]["Chain"] = LLMChain(llm=self.Chains[ConversationID]["Model"], prompt=self.Chains[ConversationID]["Prompt"])
        else:
            self.Chains[ConversationID]["Chain"] = LLMChain(llm=self.Chains[ConversationID]["Model"], prompt=self.Chains[ConversationID]["Prompt"], memory=self.Chains[ConversationID]["Conversation_Memory_inst"])

        return True

    '''
        LLM 대화
    '''
    def Start_Conversation(self, ConversationID:str, Input:str)->Optional[Dict]:
        output = None
        if (not self.Check_exists_ConversationID(ConversationID)):
            return output  # 이미 존재하지 않으면 실패

        if (not self.Chains[ConversationID]["Chain"]):
            return output # 이미 존재하지 않으면 실패

        #output = self.Chains[ConversationID]["Chain"].predict(ConversationID)
        output = self.Chains[ConversationID]["Chain"].invoke({
            "input": Input
        })

        #if(output):
            #self.Chains[ConversationID]['Conversation_Memory_inst'].chat_memory.add_user_message(Input)
            #self.Chains[ConversationID]['Conversation_Memory_inst'].chat_memory.add_ai_message(output['text'])


        return output

    '''
        잡다한 것
    '''
    # Chains 리스트 딕셔너리 변수에 ConversationID 키가 존재하는가?
    def Check_exists_ConversationID(self, ConversationID:str)->bool:
        if ConversationID in self.Chains:
            return True
        else:
            return False
    '''
        대화 삭제
    '''
    def Terminate_Conversation(self, ConversationID:str)->bool:
        if (not self.Check_exists_ConversationID(ConversationID)):
            return False  # 이미 존재하지 않으면 실패
        self.Chains.pop(ConversationID)
        return True


inst = LLM_Manager()
inst.Init_Select_Model("ABC", Ollama(base_url='http://192.168.0.100:11434', model='gemma2'))
inst.Init_Conversation_Memory('ABC', True)

# 선택임
inst.Conversation_Memory_add_SystemMessage('ABC', '너는 한국어만 하는 챗봇. 문장은 최대 3개만 응답.')

# 선택임
inst.Conversation_Memory_add_userMessage('ABC', '너는 너의 이름을 알아?')
inst.Conversation_Memory_add_aiMessage('ABC', '저는 저의 이름을 모르겠어요')
inst.Conversation_Memory_add_userMessage('ABC', '너의 이름은 COMINAM이야')

inst.Set_Prompt('ABC', '너는 훌륭하고 완벽한 한국어 전용 챗봇이다. 이전 대화를 참조하여 자연스럽게 응답하라.')
inst.Set_Chain("ABC")



r = inst.Start_Conversation('ABC', '안녕 내 이름은 CHO야 너는? 너의 이름이 뭔지 알려줘')['text']
print(r)

r = inst.Start_Conversation('ABC', '안녕 COMINAM! 지금 뭐하는지 알려줄래?')['text']
print(r)
