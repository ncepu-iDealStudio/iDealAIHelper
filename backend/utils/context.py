#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File : context.py
@Time : 2023/04/16 16:17:34
@Author : Jackiex 
@Version : 1.0
@License : (C)Copyright 2022-2023
@Desc : None
'''

'''
 please input your comment about this file!
'''


class ContextHandler(object):
    def __init__(self, max_context=3200, context_del_config=None):
        super().__init__()
        self.context = []
        self.role_lengths = []
        self.max_context = max_context

        # the config of del context
        self.context_del_config = context_del_config

    def append_cur_to_context(self, data, complete__length, tag=0):

        if tag == 0:
            role = "user"
        elif tag == 1:
            role = "assistant"
        else:
            role = "system"

        role_data = {"role": role, "content": data}
        self.context.append(role_data)
        self.role_lengths.append(complete__length)

    def cut_context(self, cur_total_length, tokenizer):
        if self.context_del_config:
            del_context(self.context, self.role_lengths, cur_total_length, self.max_context, tokenizer=tokenizer,
                        distance_weights=self.context_del_config.distance_weights,
                        length_weights=self.context_del_config.length_weights,
                        role_weights=self.context_del_config.role_weights,
                        sys_role_ratio=self.context_del_config.sys_role_ratio,
                        del_ratio=self.context_del_config.del_ratio,
                        max_keep_turns=self.context_del_config.max_keep_turns,
                        )
        # use the default pram
        else:
            del_context(self.context, self.role_lengths,
                        cur_total_length, self.max_context, tokenizer=tokenizer)

    def clear(self):
        self.context.clear()


def del_context(dialogue_context, dialogue_lengths, cur_total_length, max_length, tokenizer,
                distance_weights=0.05,
                length_weights=0.4,
                role_weights=1,
                sys_role_ratio=3,
                del_ratio=0.4,
                max_keep_turns=30,
                ):
    dia_nums = len(dialogue_context)

    # if the dia_nums exceeded max_keep_turns turns,del the oldest dia

    sys_role_weights = role_weights * sys_role_ratio

    is_cut_finished = False
    while dia_nums > max_keep_turns:

        dialogue_context.pop(0)

        cur_pop_length = dialogue_lengths[0]
        dialogue_lengths.pop(0)

        cur_total_length -= cur_pop_length

        dia_nums -= 1

        if cur_total_length <= max_length:
            is_cut_finished = True
            break

    if is_cut_finished:
        return dialogue_context, dialogue_lengths

    del_score_list = []
    for dia_id in range(dia_nums):
        distance = dia_nums - dia_id
        length = dialogue_lengths[dia_id]
        content = dialogue_context[dia_id]

        if content['role'] == 'assistant':
            cal_role_weights = sys_role_weights
        else:
            cal_role_weights = role_weights

        dia_score = (distance*distance_weights + length /
                     max_length*length_weights)*cal_role_weights
        del_score_list.append(dia_score)

    del_indexes = argsort(del_score_list, reverse=True)

    del_id = 0
    while cur_total_length > max_length:

        if del_id == dia_nums - 1:
            raise Exception(
                "the remain dialogue after context cutting still too long")

        del_dia = dialogue_context[del_indexes[del_id]]
        del_dia_length = dialogue_lengths[del_indexes[del_id]]

        exceed_num = cur_total_length - max_length
        # delete the del_ratio numbers at most for each dialogue
        ch_del_dia_len = len(del_dia['content'])
        if exceed_num/del_dia_length < del_ratio:
            # +2 for token "/n"
            del_st_index = int((exceed_num/del_dia_length)*ch_del_dia_len)+2
        else:
            del_st_index = int(del_ratio*ch_del_dia_len)

        deleted_dia = del_dia['content'][del_st_index:]
        deleted_dia_length = tokenizer.num_tokens_from_string(deleted_dia)

        cur_total_length -= (del_dia_length - deleted_dia_length)

        dialogue_context[del_indexes[del_id]]['content'] = deleted_dia
        dialogue_lengths[del_indexes[del_id]] = deleted_dia_length

        del_id += 1

    return dialogue_context, dialogue_lengths
