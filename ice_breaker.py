from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
import os
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

def ice_break_with(name:str) -> str:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username, mock=True)

    summary_template = """
            given the information {information} about a person I want you to create:
            1. A short summary
            2. two interesting facts about them
            """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOpenAI(
        temperature=0,
        model_name=os.environ["OPENAI_API_MODEL"],
        # openai_api_base=os.environ["OPENAI_API_BASE"],
    )

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    # linkedin_data = scrape_linkedin_profile(linkedin_profile_url="", mock=True)
    res = chain.invoke(input={"information": linkedin_data})

    print("res", res)

if __name__ == "__main__":
    load_dotenv()

    ice_break_with("Zainul Abideen")
