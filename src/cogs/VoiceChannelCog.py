
from discord import ext, Object, Member, VoiceState, VoiceClient, app_commands, Interaction
from discord.ext import commands, tasks
from src.voicestate.CQueue import CQueue
import asyncio

from torch import nn
import torch

from src.voicestate.CVoiceState import CVoiceState
from src.voicestate.events.VoiceclientEvents import Join, Leave
from transformers import BertForSequenceClassification, AutoTokenizer, pipeline


class VoiceChannelCog(ext.commands.Cog):
    # {'member': member, 'state': state}
    #TODO: Fare una coda asincrona che tiene conto le varie operazione che il bot deve fare
    def __init__(self, bot: ext.commands.Bot):
        #self.__voice_state = CVoiceState(bot.loop)
        #self.__queue = CQueue()
        self.__vc: VoiceClient | None = None
        self.__bot = bot
        #
        # model_name = "dbmdz/bert-base-italian-xxl-cased"
        # #
        # tokenizer = AutoTokenizer.from_pretrained(model_name)
        # #
        # model = BertForSequenceClassification.from_pretrained(model_name, num_labels=3)
        # # nlp = pipeline("sentiment-analysis", model=pt_model, tokenizer=tokenizer)
        # # results = nlp('cosa cazzo fai coglione!')
        # # print(results)
        #
        # sentence = 'Huggingface è un team fantastico!'
        # input_ids = tokenizer.encode(sentence, add_special_tokens=True)
        #
        # # Create tensor, use .cuda() to transfer the tensor to GPU
        # tensor = torch.tensor(input_ids).long()
        # # Fake batch dimension
        # tensor = tensor.unsqueeze(0)
        #
        # # Call the model and get the logits
        # logits, = model(tensor)
        #
        # # Remove the fake batch dimension
        # logits = logits.squeeze(0)
        #
        # # The model was trained with a Log Likelyhood + Softmax combined loss, hence to extract probabilities we need a softmax on top of the logits tensor
        # proba = nn.functional.softmax(logits, dim=0)
        #
        # # Unpack the tensor to obtain negative, neutral and positive probabilities
        # negative, neutral, positive = proba
        #
        # print(neutral)


    @ext.commands.Cog.listener()
    async def on_ready(self):
        #self.__run.start()
        ...

    @app_commands.command(
        name='join',
        description='Join the voice channel.'
    )
    async def join(self, interaction: Interaction):
        print('a')
        vc = await interaction.user.voice.channel.connect()
        print('c')

    @app_commands.command(
        name='play',
        description='Play a song.'
    )
    async def play(self, interaction: Interaction):
        self.__vc.play("/Users/alessandro/Desktop/TyrLawbringerDiscordBot/Tyr_Kill_Tower_1.oga")

    def cog_unload(self):
        self.__run.cancel()

    @tasks.loop()
    async def __run(self):
        while True:
            print('Waiting')
            element = await asyncio.wait_for(self.__queue.get(), timeout=None)
            print('Event!')
            await self.__on_user_event(element['state'], element['event'])

    async def __on_user_event(self, state: VoiceState, event: Join | Leave):
        print('1')
        if state.channel.members:
            print('2')
            if self.__bot.application.id not in [m.id for m in state.channel.members]:
                await self.__voice_state.join(state.channel)

    async def __join(self, state):
        self.__vc = await state.channel.connect()

    @ext.commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        ...
        # print('Update')
        # if not before.channel and after.channel:
        #     state = after
        #     event = Join()
        #     print(' Join')
        # elif before.channel and not after.channel:
        #     state = before
        #     event = Leave()
        #     print(' Leave')
        # else:
        #     return None
        #
        # self.__queue.add({
        #     'state': state,
        #     'event': event
        # })


async def setup(bot: ext.commands.Bot):
    await bot.add_cog(VoiceChannelCog(bot), guilds=[Object(id=928785387239915540)])