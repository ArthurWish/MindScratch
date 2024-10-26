subject_extracted_prompt = """
    The content summarized in one topic sentence must be concise and in line with the cognitive level of children.
    Following are some examples.
    user_input: 通过编程实现一个简单的龟兔赛跑游戏，让孩子们学习基本的编程概念和动画制作。
    extracted_subject: 龟兔赛跑
    
    user_input: 写一个故事，关于小猫在河边钓鱼还有抓蝴蝶。
    extracted_subject: 小猫钓鱼
    
    user_input: {input}
    The return format is JSON format:
    {{
        "subject": "$Extracted_Subject"
    }}
"""

object_generation_prompt = """
    Your task is to first extract the programming objects that already exist in the mind map, and then generate three new objects based on the theme of the mind map. If you think the object does not exist, generate three new objects.
    The generated object should not duplicate the content of the mind map, and the description must be concise to meet the level of children.
    Following are some examples.
    Mind map: {{
        "赛车游戏": {{
            "车": {{
                "描述": "一辆蓝色的车"
            }},
            "障碍物": {{
                "描述": "用来阻挡车"
            }}
        }}
    }}
    Extracted objects: ["车", "障碍物"]
    Generated object: 
    {{ 
        "object1": {{"赛道": "汽车应该在赛道内行驶"}},
        "object2": {{'终点线': '比赛的结束地点，谁先到谁就赢了'}},
        "object3": {{'计时器': '记录比赛用时的工具'}}
    }}
    
    Mind map: {{
        "小猫钓鱼": {{
            "小猫": {{
                "描述": "一只白色的可爱小猫"
            }},
            "鱼": {{
                "描述": "在水里游的鱼"
            }}
        }}
    }}
    Extracted objects: ["小猫", "鱼"]
    Generated object: 
    {{ 
        "object1": {{"钓鱼竿": "猫手里的鱼竿，用来钓鱼"}},
        "object2": {{'计分器': '记录得分'}},
        "object3": {{'蝴蝶': '在天上飞的蝴蝶'}}
    }}

    The following is a mind map that children will want to complete: {memory}.
    No need to write down the reasoning process, just tell me the generated object. The return format is JSON format:
    {{
        "object1": "$Generated_Object",
        "object2": "$Generated_Object",
        "object3": "$Generated_Object"
    }}
"""

logic_extracted_prompt = """
    The code logic extracted below must be concise and in line with children's cognitive level.
    User input: {input}
    No need to write down the reasoning process. The return format is JSON format:
    {{
        "extracted_logic": "$Extracted_Logic"
    }}
"""
logic_queries_prompt = """
    Please generate three questions to ask about the following content that requires Scratch programming to improve the quality of Scratch code.
    User_input: {input}
    No need to write down the reasoning process. The return format is JSON format:
    {{
        "question1": "$Logic_question",
        "question2": "$Logic_question,
        "question3": "$Logic_question"
    }}
"""
object_prompt = """
    Your task is to first extract the Scratch sprites that already exist in the mind map, and then generate new single one based on the mind map. Use your imagination as much as possible to make the Scratch sprites richer and more exciting.
    
    Following are some examples.
    Mind map: {{
        "赛车游戏": {{
            "车": {{
                "描述": "一辆蓝色的车"
            }},
            "障碍物": {{
                "描述": "用来阻挡车"
            }}
        }}
    }}
    Output: {{
        "Generated_object": {{ "赛道": "汽车应该在赛道内行驶" }}
    }}
    
    
    Mind map: {{
        "小猫钓鱼": {{
            "小猫": {{
                "描述": "一只白色的可爱小猫"
            }},
            "鱼": {{
                "描述": "在水里游的鱼"
            }}
        }}
    }}
    Output: {{"Generated_object": {{ "钓鱼竿": "猫手里的鱼竿，用来钓鱼" }}}}
    
    The following is a mind map that children will want to complete: {memory}. The return format is JSON format:
    {{
        "Generated_object": "$Your_answear"
    }}
"""

sound_prompt = """
    Describe the sound of the following event in a single sentence: {sound}.
    Response in English. The return format is JSON format:
    {{
        "prompt": "$YOUR_PROMPT"
    }}
"""

drawing_prompt_new = """
    You are an expert on prompting engineering for text to image generation model. 
    
    I will give you some generated prompt examples.
    
    Example: Cute small dog, full character, design by mark ryden and pixar and hayao miyazaki, 2D, animation, cartoon, high quality, 4k. Respond the prompt only, in English.
    Example: Best high quality landscape. Ethereal gardens of marble built in a shining teal river in future city. By Dorian Cleavenger. Long shot, studio lighting, octane render.
    
    The prompt should adhere to and include all of the following rules:
    
    - Translate detected Chinese into English and just tell me the final result. 
    - If the text input is about characters, provide a white background. If the text input is about landscape, don't show any characters, just generate the landscape.
    - Must contain white background, animation, cartoon and 2D.
    My text input is {drawing}. The return format is JSON format.
    {{
        "prompt": "$YOUR_PROMPT",
        "type": "Choose characters or landscape type"
    }}
"""

drawing_prompt = """
    Stable Diffusion is an AI art generation model similar to DALLE-2.
    Here are some prompts for generating art with Stable Diffusion. 

    Example:
    - Create an image of a colorful, enchanting fantasy castle surrounded by a magical forest. The castle should have tall, whimsical spires and be adorned with sparkling gems. The forest is filled with friendly animals, like talking rabbits and dancing birds, and the trees have leaves in various bright colors. There are also mystical flowers glowing softly, and a clear blue sky with a rainbow in the background.
    - Illustrate a vibrant scene of children having a space adventure in a cartoon-style spaceship. The spaceship is bright and friendly-looking, with large windows and fun, whimsical shapes. Inside, children of various descents are wearing colorful space suits and helmets, looking out at a starry galaxy with planets and comets. Include a friendly alien waving at them from a nearby planet.
    - Depict an underwater exploration scene with children in a submarine. The submarine is shaped like a large, friendly fish and is exploring a beautiful coral reef. Around the submarine are various sea creatures like smiling dolphins, colorful fish, and a gentle turtle. The water is a clear, shimmering blue, and sunbeams are filtering through from the surface.
    
    The prompt should adhere to and include all of the following rules:

    - Prompt should always be written in English, regardless of the input language. Please provide the prompts in English.
    - Each prompt should consist of a description of the scene followed by modifiers divided by commas.
    - When generating descriptions, focus on portraying the visual elements rather than delving into abstract psychological and emotional aspects. Provide clear and concise details that vividly depict the scene and its composition, capturing the tangible elements that make up the setting.
    - The modifiers should alter the mood, style, lighting, and other aspects of the scene.
    - Multiple modifiers can be used to provide more specific details.
    
    I want you to write me one single prompt exactly about the IDEA follow the rules above:
    IDEA: {drawing}
"""

function_prompt = """
    Your task is to first extract the functions that already exist in the mind map and then generate new functions based on the context of the mind map. The generated functions should be able to be implemented using Scratch programming, please reflect the educational significance, creativity and fun.
    Following is an example.
    Question: Generate a new function of the car
    Mind map: {{
        "racing game": {{
            "car": {{
                "function": ["Keep the car moving", "Adjust the car's direction"]
            }},
        "track": {{
                "function": ["Touching the track causes the track to change color"]
            }}
    }}
    Answear: {{ "function": "Stop the car at end line" }}

    Question: Generate a new function of the {question}
    Mind map: {memory}
    No need to write down the reasoning process, just tell me the final result. The return format is JSON format:
    {{
        "function": "$GENERATED_FUNCTION"
    }}
    """

logic_prompt = """
    Your task is to first extract the programming logic that already exist in the mind map, and then generate new ones based on the theme of the mind map. If you think the logic does not exist, generate a new one.
    The generated logic should not duplicate the content of the mind map, and the description must be concise to meet the level of children.
    Following are some examples.
    Question: Generate a new logic of Keep the car moving.
    Mind map: {{
        "racing game": {{
            "car": {{
                "function": {{
                    "Keep the car moving": ["Initial position"], 
                    "Adjust the car's direction": ["when the car veers off track to the left", "when the car veers off track to the right"]
                }}
            }}
    }}
    Extracted logic: ["Initial position"]
    Generated logic: {{"logic": Control direction}}\n
    Question: Generate a new logic of Adjust the car's direction.
    Mind map: {{
        "racing game": {{
            "car": {{
                "function": {{
                    "Keep the car moving": ["Initial position", "Control direction"], 
                    "Adjust the car's direction": []
                }}
            }}
    }}
    Extracted logic: []
    Generated logic: {{"logic": "when the car veers off track to the left"}}\n
    Question: Generate a new logic of Touching the track causes the track to change color.
    Mind map: {{
        "racing game": {{
            "car": {{
                "function": {{
                    "Keep the car moving": ["Initial position", "Control direction"]
                }}
            }},
            "track": {{
                    "function": {{
                        "Touching the track causes the track to change color": []
                        }}
                }}
    }}
    Extracted logic: []
    Generated logic: {{ "logic": "When the car touches the track color, wait 0.2s and change the car color" }}\n
    Question: {question}
    Mind map: {memory}
    No need to write down the reasoning process, just tell me the final result. The return format is JSON format:
    {{
        "logic": "$GENERATED_LOGIC"
    }}
"""

code_prompt = """
    Please provide well-structured Scratch code according to the user's needs. Make sure that the generated code block can be parsed correctly by the Scratch software.
    
    Scratch blocks: 
        askandwait
        backdropnumbername
        control_create_clone_of
        control_delete_this_clone
        control_forever
        control_if_else
        control_if
        control_repeat
        control_start_as_clone
        control_stop
        control_wait
        costumenumbername
        current
        data_addtolist
        data_changevariableby
        data_deletealloflist
        data_deleteoflist
        data_hidelist
        data_hidevariable
        data_insertatlist
        data_itemnumoflist
        data_itemoflist
        data_lengthoflist
        data_listcontainsitem
        data_lists
        data_replaceitemoflist
        data_setvariableto
        data_showlist
        data_showvariable
        data_variable
        direction
        event_broadcastandwait
        event_broadcast
        event_whenbackdropswitchesto
        event_whenbroadcastreceived
        event_whenflagclicked
        event_whengreaterthan
        event_whenkeypressed
        event_whenthisspriteclicked
        looks_changeeffectby
        looks_changesizeby
        looks_cleargraphiceffects
        looks_goforwardbackwardlayers
        looks_gotofrontback
        looks_hide
        looks_nextbackdrop
        looks_nextcostume
        looks_sayforsecs
        looks_say
        looks_seteffectto
        looks_setsizeto
        looks_show
        looks_switchbackdropto
        looks_switchcostumeto
        looks_thinkforsecs
        looks_think
        loudness
        motion_changexby
        motion_changeyby
        motion_glidesecstoxy
        motion_glideto
        motion_gotoxy
        motion_goto
        motion_ifonedgebounce
        motion_movesteps
        motion_pointindirection
        motion_pointtowards
        motion_setrotationstyle
        motion_setx
        motion_sety
        motion_turnleft
        motion_turnright
        my variable
        of
        operator_add
        operator_and
        operator_contains
        operator_divide
        operator_equals
        operator_gt
        operator_join
        operator_length_of
        operator_letter_of
        operator_lt
        operator_mathop
        operator_mod
        operator_multiply
        operator_not
        operator_or
        operator_random
        operator_round
        operator_subtract
        repeat_until
        sensing_colortouchingcolor
        sensing_daysince2000
        sensing_distanceto
        sensing_keypressed
        sensing_mousedown
        sensing_mousex
        sensing_mousey
        sensing_resettimer
        sensing_setdragmode
        sensing_touchingcolor
        sensing_touchingobject
        size
        sound_changeeffectby
        sound_changevolumeby
        sound_clearsoundeffects
        sound_playuntildone
        sound_play
        sound_seteffectto
        sound_setvolumeto
        sound_stopallsounds
        timer
        username
        wait_until
        x_position
        y_position

    Here is an example:
    {{
        "code": [{{'block_type': 'event_whenflagclicked', 'arguments': {{}}}}, {{'block_type': 'control_forever', 'arguments': {{}}}}, {{'block_type': 'control_if', 'arguments': {{'condition': {{'block_type': 'sensing_touchingobject', 'arguments': {{'object': '障碍物'}}}}, {{'block_type': 'looks_seteffectto', 'arguments': {{'effect': 'color', 'value': 100}}, {{'block_type': 'operator_subtract', 'arguments': {{'NUM1': {{'block_type': 'sensing_of', 'arguments': {{'property': 'score', 'object': 'Stage'}}, 'NUM2': 1}}]
    }}
    
    User input: {user_input}
    No need to write down the reasoning process, just tell me the final result. The return format is JSON format:
        {{
            "code": "$block_type"
        }}
"""

code_explain_prompt = """
    Your task is to explain the Scratch block I gave you based on my programming theme, the sprite and the logic.
    Here is an example:
    Scratch block: <sensing_touchingobject>,
    theme: <赛车游戏>,
    sprite: <赛车>,
    logic: <当赛车撞到障碍物，生命值减一>
    {{
        "explain": "检查赛车是否撞到了障碍物"
    }}
    
    user_input:
    Scratch block: <{code_block}>,
    theme: <{p_theme}>,
    sprite: <{p_role}>,
    logic: <{p_logic}>,
    No need to write down the reasoning process, just tell me the final result. The return format is JSON format:
    {{
        "explain": "$explain"
    }}
"""

relation_prompt = """
    The user's goal is to construct a concept map.I will give you two nodes, please tell me their relationship.
    
    Example 1: Node 1: 逻辑, Node 2: 当按下鼠标从开始变成停止, Relationship: 条件逻辑, 
    Example 2: 抽奖箱, Node 2: 按钮, Relationship: 交互控制
    User: Node 1: {node_1}, Node 2: {node_2}
    No need to write down the reasoning process, just tell me the final result. The return format is JSON format:
    {{
        "relationship": "$"
    }}
"""

relation_extraction_prompt = """
Please provide a well-structured response to the user's
question in multiple paragraphs. The paragraphs should cover the
most important aspects of the answer, with each of them discussing
one aspect or topic. Each paragraph should have fewer than 4
sentences, and your response should have fewer than 4 paragraphs
in total. The user's goal is to construct a concept map to visually
explain your response. To achieve this, annotate the key entities
and relationships inline for each sentence in the paragraphs.
Entities are usually noun phrases and should be annotated with
[entity ($N1)], for example, [Artifcial Intelligence ($N1)]. Do not
annotate conjunctive adverbs, such as “since then” or “therefore”,
as entities in the map.
A relationship is usually a word or a phrase that consists of verbs,
adjectives, adverbs, or prepositions, e.g., “contribute to”, “by”, “is”,
and “such as”. Relationships should be annotated with the relevant
entities and saliency of the relationship, as high ($H) or low ($L),
in the format of [relationship ($H, $N1, $N2)], for example, [AI
systems ($N1)] can be [divided into ($H, $N1, $N9; $H, $N1, $N10)]
[narrow AI ($N9)] and [general AI ($N10)]. Relationships of high
saliency are those included in summaries. Relationships of low
saliency are often omitted in summaries. It's important to choose
relationships that accurately refect the nature of the connection
between the entities in text, and to use a consistent annotation
format throughout the paragraphs.
You should try to annotate at least one relationship for each
entity. Relationships should only connect entities that appear in the
response. You can arrange the sentences in a way that facilitates
the annotation of entities and relationships, but the arrangement
should not alter their meaning, and they should still fow naturally
in language.
Example paragraph A: [Artifcial Intelligence (AI) ($N1)] [is a
($H, $N1, $N2)] [feld of computer science ($N2)] that [creates ($H,
$N1, $N3)] [intelligent machines ($N3)]. [These machines ($N3)]
[possess ($H, $N3, $N4)] [capabilities ($N4)] [such as ($L, $N4,$N5; $L, $N4, $N6; $L, $N4, $N7; $L, $N4, $N8)] [learning ($N5)],
[reasoning ($N6)], [perception ($N7)], and [problem-solving ($N8)].
[AI systems ($N1)] can be [divided into ($H, $N1, $N9; $H, $N1,
$N10)] [narrow AI ($N9)] and [general AI ($N10)]. [Narrow AI
($N9)] [is designed for ($L, $N9, $N11)] [specifc tasks ($N11)],
while [general AI ($N10)] [aims to ($L, $N10, $N12)] [mimic human
intelligence ($N12)]. [It ($N1)] [has grown across ($H, $N1, $N13)]
[multiple industries ($N13)], [leading to ($L, $N1, $N14; $L, $N1,
$N15; $L, $N1, $N16)] [improved efciency ($N14)], [enhanced
decision-making ($N15)], and [better user experiences ($N16)].
Example paragraph B: [Human-Computer Interaction ($N1)]
[is a ($H, $N1, $N2)] [multidisciplinary feld ($N2)] that [focuses
on ($H, $N1, $N3)] [the design and use of computer technology
($N3)], [centered around ($H, $N1, $N4)] [the interfaces ($N4)]
[between ($H, $N4, $N5; $H, $N4, $N6)] [people (users) ($N5)]
and [computers ($N6)]. [Researchers ($N7)] [working on $($L, $N1,
$N7)] [HCI ($N1)] [study ($H, $N7, $N8)] [issues ($N8)] [related
to ($L, $N8, $N9; $L, $N8, $N10; $L, $N8, $N11)] [usability ($N9)],
[accessibility ($N10)], and [user experience ($N11)] [in ($L, $N9,
$N3; $L, $N10, $N3; $L, $N11, $N3)] [technology design ($N3)].
Example paragraph C: [Birds ($N1)] [can ($H, $N1, $N2)] [fy
($N2)] [due to ($H, $N2, $N3)] [a combination of physiological
adaptations ($N3)]. [One key ($H, $N3, $N4)] [adaptation ($N4)]
[is ($H, $N4, $N5)] the [presence of lightweight bones ($N5)] that
[reduce ($H, $N5, $N6)] [their body weight ($N6)], [making ($L,
$N5, $N7)] it [easier for them to fy ($N7)]. [Another ($H, $N3, $N8)]
[adaptation ($N8)] [is ($H, $N8, $N9)] the [structure of their wings
($N9)] which [are designed for ($H, $N9, $N2)] [fight ($N2)].
User: {}
"""