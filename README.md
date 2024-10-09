# LangChain_PART_1
랭체인 기반으로 이전대화를 기록하는 LLM을 쉽게 사용할 수 있는 도구 레포지토리입니다. 

<br>

---

# 사용하는 법


1. 먼저 Class 인스턴스를 생성합니다.
```python
inst = LLM_Manager()
```

<br>

2. (1.)에 생성한 인스턴스에 "Init_Select_Model"을 최초 호출하여 LLM모델 객체와 함께 등록합니다.
<br>2-1. 1번째 매개변수는 앞으로 저장할 딕셔너리의 key 값입니다.
<br>2-2. 2번째 매개변수는 LLM모델 객체입니다.
```python
inst.Init_Select_Model("ABC", Ollama(base_url='http://192.168.0.100:11434', model='gemma2'))
```

<br>

3. "Init_Conversation_Memory"를 호출하여 "대화 메모리"객체를 최초 등록합니다. ( Option )
```python
inst.Init_Conversation_Memory('ABC', True)
```

<br>

4. "Conversation_Memory_add_SystemMessage"를 호출하여 "Prompt"에서가 아닌, "Memory"에 System을 등록합니다. ( Option )
```python
inst.Conversation_Memory_add_SystemMessage('ABC', '너는 완벽한 응답을 하는 챗봇이야. 그리고 너는 오직 한국어만 응답할 수 있다.')
```

<br>

5. 추가적으로 Conversation_Memory_add_userMessage, Conversation_Memory_add_aiMessage를 통하여 사전에 질의응답을 생성할 수 있습니다. 
```python
inst.Conversation_Memory_add_userMessage('ABC', '넌 누구야?')
inst.Conversation_Memory_add_aiMessage('ABC', '저는 EDR제품사에서 개발된 챗봇이에요')
```

<br>

6. 필수요소인, Prompt는 "Set_Prompt"를 호출하여 생성합니다.
```python
inst.Set_Prompt('ABC', '너는 훌륭한 한국어 전용 챗봇이다.')
```

<br>

7. "Set_Chain"는 체인을 생성합니다. (1~부터 순차적으로 성공한다면 체인을 제대로 생성할 수 있습니다 )
```python
inst.Set_Chain("ABC")
```

<br>

8. 자 이제 대화를 해야겠죠? "Start_Conversation"를 호출하여 시작합니다
```python
r = inst.Start_Conversation('ABC', '안녕하세요')['text']
print(r)
```

---

<br>

# 참고할 사항은 무엇인가?

이 파이썬 코드는 1개의 Class로 구성되어 있습니다.

이 Class는 "이전 대화를 기억하는 LLM"을 쉽고 빠르게 구성하고 사용할 수 있도록 구현되었습니다. 

<br>

Sample코드가 내장되어 있으며, 추가 및 사용하시면 됩니다.

LLM을 추가하는 과정에서 Sample코드에서는 "Ollama"를 사용하였지만, OpenAPI든 모두 사용이 가능합니다.

<br>

*기본 랭체인 모듈을 사용하였으므로, 경고창이 뜰 수 있습니다. 

---
