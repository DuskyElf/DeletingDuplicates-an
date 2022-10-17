import manim as m

class DeleteDuplicate(m.Scene):
    def construct(self):
        title = m.Text("Deleting Duplicates in a String")
        self.play(m.Write(title), run_time=1)
        self.play(title.animate.to_edge(m.UP), run_time=0.75)

        code_block = m.Text(
            "def delete_duplicates( test_case )\n"\
            "    foreach ch in test_case\n"\
            "        if char_stack.not_empty()\n"\
            "            if ch == test_case.last()\n"\
            "                char_stack.pop()\n"\
            "                continue\n"\
            "        char_stack.push( ch )\n"\
            "    return str( char_stack )",
            font='Hack Nerd Font',
            t2c={
                'def':              m.LIGHT_PINK,
                'foreach':          m.LIGHT_PINK,
                'in ':              m.LIGHT_PINK,
                'if':              m.LIGHT_PINK,
                'continue':         m.LIGHT_PINK,
                'return':           m.LIGHT_PINK,
                'delete_duplicates':m.BLUE,
                'test_case':        m.BLUE,
                ' ch ':             m.BLUE,
                'char_stack':       m.BLUE,
                'str':              m.BLUE,
                'not_empty':        m.YELLOW,
                'last':             m.YELLOW,
                'pop':              m.YELLOW,
                'push':             m.YELLOW
            }
        ).scale(0.5)
        code_block.to_edge(m.DR, buff=0.75)
        self.play(m.Create(code_block))
        self.wait()

        string = m.Text('"abbaca"', color=m.GREEN)
        string.next_to(title, m.DOWN, buff=1.75)
        string.to_edge(m.LEFT, buff=1)
        string.scale(0.8)
        self.play(
            m.AnimationGroup(*[m.FadeIn(i) for i in string], lag_ratio=0.15),
            run_time = 1
        )
        self.wait(0.25)

        string_surrounder = m.SurroundingRectangle(string, color=m.BLUE, buff=0.3)
        string_identifier = m.Text("test_case").scale(0.7)
        string_identifier.next_to(string_surrounder, m.UP)
        self.play(m.Create(string_surrounder), m.Write(string_identifier))
        self.wait()

        list_start = m.Text("[")
        list_end = m.Text("]")
        list_start.scale(0.8)
        list_end.scale(0.8)
        list_start.next_to(string_surrounder, buff=3)
        list_end.next_to(list_start)
        test_case = 'abbaca'
        list_elements = m.VGroup(*[m.Text(f"'{i}'", color=m.GREEN) for i in test_case])
        list_elements.scale(0.8)
        list_identifier_t = m.Text("char_stack").scale(0.7)
        list_identifier = m.always_redraw(
            lambda: list_identifier_t.next_to(m.VGroup(list_start, list_end), m.UP, buff=0.5)
        )
        self.play(
            m.Write(list_start),
            m.Write(list_end),
            m.Write(list_identifier),
            run_time=0.5
        )
        self.wait()

        self.algo_nop(list_elements[0], string[1], list_start, list_end)
        self.algo_nq(list_elements[0], list_elements[1], string[2].copy(), list_end)
        self.algo_eq(list_elements[1], list_elements[2], string[3].copy(), list_end, list_elements[0])
        self.algo_eq(list_elements[0], list_elements[3], string[4].copy(), list_end, list_start)
        self.algo_nop(list_elements[4], string[5], list_start, list_end)
        self.algo_nq(list_elements[4], list_elements[5], string[6].copy(), list_end)
        self.wait()

        result_string = m.Text('"ca"', color=m.GREEN)
        result_string.shift(m.LEFT * 3)
        result_string.shift(m.DOWN * 2)
        self.play(
            m.ReplacementTransform(
                m.VGroup(list_start, list_end, list_elements[4], list_elements[5]).copy(),
                result_string
            )
        )
        self.play(m.Create(m.SurroundingRectangle(result_string, color=m.PINK, buff=0.25)))
        self.wait(0.25)

    def algo_nop(self, pushable, original, prev, end):
        pushable.next_to(prev)
        self.play(
            m.ReplacementTransform(original.copy(), pushable),
            end.animate.next_to(pushable)
        )
        self.wait(0.75)

    def algo_nq(self, popable, pushable, original, end):
        pushable.next_to(popable, m.DOWN)
        self.play(
            m.ReplacementTransform(original, pushable),
        )
        compare_box = m.SurroundingRectangle(
            m.VGroup(popable, pushable)
        )
        self.play(m.Create(compare_box))
        self.play(m.FadeOut(compare_box))
        self.play(
            pushable.animate.next_to(popable),
            end.animate.next_to(pushable.copy().next_to(popable))
        )

    def algo_eq(self, popable, pushable, original, end, prev):
        pushable.next_to(popable, m.DOWN)
        self.play(
            m.ReplacementTransform(original, pushable)
        )
        compare_group = m.VGroup(popable, pushable)
        compare_box = m.SurroundingRectangle(compare_group)
        self.play(m.Create(compare_box))
        self.play(m.Indicate(m.VGroup(compare_group, compare_box)))
        self.play(
            m.FadeOut(m.VGroup(compare_group, compare_box)),
            end.animate.next_to(prev)
        )
