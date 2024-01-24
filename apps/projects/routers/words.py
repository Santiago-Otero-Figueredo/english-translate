from fastapi import APIRouter, status, Depends, Request, Form, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import Session

from fastapi.templating import Jinja2Templates

from core.database import get_session

# from apps.projects.models import Task, Priority, Project, State
from apps.projects.models import Word, WordClassification, WordType, Verb
from apps.projects.schemas.detail_model import DetailModelRequest
from apps.projects.schemas.words import WordRegister, WordCompleteInfoRegister, ExampleTranslatesRequest, WordSearchRequest, TranslationRequest, ExampleRequest

from typing import Union, List

import json


templates = Jinja2Templates(directory='templates/')

router = APIRouter(
    prefix='/words',
    tags=['words'],
    responses= {404: {'description': 'Not Found'}}
) 


# @router.get('/list', status_code=status.HTTP_201_CREATED, response_class=HTMLResponse,  name='list-tasks')
# async def list_task(request: Request, filter_state:str = Query(default=None), session: Session = Depends(get_session)):
#     context = {}
#     filter = {}
#     if filter_state:
#         state_result = await State.get_by_id(int(filter_state), session)
#         filter['state_id'] = int(filter_state)
#         context['color_filter'] = state_result.color

#     context.update(filter)
#     tasks = await Task.get_by_filter(session, filter, order_by = {'update_at': 'asc'})
#     priorities = await Priority.get_all(session)
#     projects = await Project.get_all(session)
#     states = await State.get_all(session)

#     context.update({'request': request,'tasks':tasks, 'priorities': priorities, 'projects': projects, 'states': states})

#     return templates.TemplateResponse('tasks/register.html', context=context)
@router.get('/list', status_code=status.HTTP_200_OK, name='list-words')
async def list_task(session: Session = Depends(get_session)) -> List[DetailModelRequest]:
    try:
        verbal_tenses = await Word.get_all(session)
        return verbal_tenses
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while fetching words")


@router.get('/register', status_code=status.HTTP_200_OK, response_class=HTMLResponse, name='register-word')
async def register_task(request: Request, session: Session = Depends(get_session)):

    context = {}
    context.update({'request': request, 'verb_select':'Verbs'})

    return templates.TemplateResponse('words/register.html', context=context)

@router.post('/register', status_code=status.HTTP_201_CREATED, name='register-word')
async def register_word(request: Request, 
                        id_original_word: Union[str, None] = Form(None),
                        original_word: str = Form(...), 
                        id_word_variation: Union[str, None] = Form(None),
                        word_variation: str = Form(...), 
                        word_types_select: str = Form(...), 
                        verbal_tense: Union[str, None] = Form(None), 
                        translates: str = Form(...),
                        examples_json: str = Form(...),
                        session: Session = Depends(get_session)):
    # Lógica para procesar los datos del formulario

    list_translates = translates.split(',')
    list_examples_json = json.loads(examples_json)
    list_examples_translations = []
    for e_t in list_examples_json:
        example = e_t['example'].strip()
        translate = e_t['translate'].strip()
        description = e_t['description'].strip()
        id_example = int(e_t['id_example'].strip()) if e_t['id_example'].strip() != '' else None
        id_translate = int(e_t['id_translate'].strip()) if e_t['id_translate'].strip() != '' else None
        list_examples_translations.append(
            ExampleTranslatesRequest(
                id_example=id_example,
                id_translate=id_translate,
                example=example,
                translate=translate,
                description=description
            )
        )

    word_register = WordCompleteInfoRegister(
        root_word=WordRegister(id=id_original_word, value=original_word),
        word_classification=WordRegister(id=id_word_variation, value=word_variation),
        id_word_type=word_types_select,
        id_verbal_tense=verbal_tense,
        translates=list_translates,
        examples_json=list_examples_translations
    )

    await Word.register_word_with_translates(session, word_register)

    return RedirectResponse(url=request.url_for('register-word'), status_code=status.HTTP_303_SEE_OTHER)


@router.get('/get/{word_search}', status_code=status.HTTP_200_OK, response_model=WordSearchRequest, name='get-info-word')
async def search_word(word_search: str, session: Session = Depends(get_session)):
    word_info = await WordClassification.get_by_value(session, word_search, case_sensitive=False)
    word_type = await WordType.get_by_value(session, 'Verbs')

    if not word_info:
        raise HTTPException(status_code=404, detail="Word not found")

    id_verbal_tense = None
    if word_info.word_type_id == word_type.id:
        word_info = await Verb.get_by_value(session, word_search, case_sensitive=False)
        
        id_verbal_tense = word_info.verbal_tense_id

    
    if word_info:

        translates = []

        translations_without_examples = [translation for translation in word_info.translations if translation.example_id is None]

        for translate_word in translations_without_examples:
            translates.append(
                TranslationRequest(
                    id=translate_word.id,
                    value=translate_word.value.strip(),
                    description=translate_word.description
                )
            )

        examples = []
        for example_word in word_info.examples:
            examples.append(
                ExampleRequest(
                    id=example_word.id,
                    value=example_word.value,
                    translation=  TranslationRequest(
                        id=example_word.translation.id,
                        value=example_word.translation.value,
                        description=example_word.translation.description
                    )
                )
            )

        word_found = WordSearchRequest(
            id_word_classification=word_info.id,
            value_word_classification=word_info.value,
            id_root_word=word_info.word_id,
            value_root_word=word_info.word.value,
            id_word_type=word_info.word_type_id,
            id_verbal_tense= id_verbal_tense,
            number_of_times_searched=word_info.number_of_times_searched,
            translates=translates,
            examples_json=examples
        )

      
        return word_found
    else:
        raise HTTPException(status_code=404, detail="Word not found")
# @router.post('/register', status_code=status.HTTP_201_CREATED, response_class=HTMLResponse, name='register-word')
# async def register_task(request: Request,
#                             name:str = Form(),
#                             description:str = Form(default=''),
#                             priority:int = Form(),
#                             project:int = Form(),
#                             session: Session = Depends(get_session)):
#     new_priority = CreateTaskRequest(
#         name=name,
#         description=description,
#         priority=priority,
#         project=project
#     )

#     #await Task.create(new_priority, session)

#     return RedirectResponse(url=request.url_for('register-word'),status_code=status.HTTP_303_SEE_OTHER)


# @router.get('/register/project/{project_id}', response_class=HTMLResponse,  name='register-by-project')
# async def register_task_by_project(request: Request, project_id:int, filter_state:str = Query(default=None), session: Session = Depends(get_session)):
#     context = {}
#     filter = {}
#     print(project_id)
#     filter['project_id'] = int(project_id)
#     if filter_state:
#         state_result = await State.get_by_id(int(filter_state), session)
#         filter['state_id'] = int(filter_state)
#         context['color_filter'] = state_result.color

#     context.update(filter)
#     context['actual_project'] = await Project.get_by_id(project_id, session)
#     tasks = await Task.get_by_filter(session, filter, order_by = {'update_at': 'desc'})
#     priorities = await Priority.get_all(session)
#     projects = await Project.get_all(session)
#     states = await State.get_all(session)

#     context.update({'request': request,'tasks':tasks, 'priorities': priorities, 'projects': projects, 'states': states})

#     return templates.TemplateResponse('tasks/projects/register.html', context=context)


# @router.post('/register/project/{project_id}', status_code=status.HTTP_201_CREATED, response_class=HTMLResponse, name='register-by-project')
# async def register_task_by_project(request: Request,
#                             project_id:int,
#                             name:str = Form(),
#                             description:str = Form(default=''),
#                             priority:int = Form(),
#                             session: Session = Depends(get_session)):
#     new_priority = CreateTaskRequest(
#         name=name,
#         description=description,
#         priority=priority,
#         project=project_id
#     )

#     await Task.create(new_priority, session)

#     return RedirectResponse(url=request.url_for('register-by-project', project_id=project_id),status_code=status.HTTP_303_SEE_OTHER)

# @router.post('/update/{task_id}', status_code=status.HTTP_200_OK, response_class=HTMLResponse, name='update-task')
# async def update_task(request: Request,
#                         task_id: int,
#                         name:str = Form(),
#                         description:str = Form(default=''),
#                         priority:int = Form(),
#                         project:int = Form(),
#                         session: Session = Depends(get_session)):

#     existing_task = await Task.get_by_id(task_id, session)

#     if existing_task is None:
#         raise HTTPException(status_code=404, detail="Task not found")

#     # Actualizar los campos
#     updated_priority = CreateTaskRequest(
#         name=name,
#         description=description,
#         priority=priority,
#         project=project
#     )
#     existing_task.update(updated_priority, session)

#     return RedirectResponse(url=request.url_for('register-by-project', project_id=project), status_code=status.HTTP_303_SEE_OTHER)



# @router.post('/delete/{task_id}', status_code=status.HTTP_204_NO_CONTENT, name='delete-task')
# async def delete_task(request: Request, task_id: int, session: Session = Depends(get_session)):
#     existing_task = await Task.get_by_id(task_id, session)
#     project_id = existing_task.project_id
#     if existing_task is None:
#         raise HTTPException(status_code=404, detail="task not found")

#     # Eliminar el registro
#     session.delete(existing_task)
#     session.commit()

#     return RedirectResponse(url=request.url_for('register-by-project', project_id=project_id), status_code=status.HTTP_303_SEE_OTHER)


# @router.post('/complete/{task_id}', status_code=status.HTTP_204_NO_CONTENT, name='complete-task')
# async def complete_task(request: Request, task_id: int, payload: CompleteTaskRequest, session: Session = Depends(get_session)):
#     existing_task = await Task.get_by_id(task_id, session)
#     if existing_task is None:
#         raise HTTPException(status_code=404, detail="task not found")

#     # Eliminar el registro
#     existing_task.complete(payload, session)

#     return RedirectResponse(url=request.url_for('list-tasks'), status_code=status.HTTP_303_SEE_OTHER)